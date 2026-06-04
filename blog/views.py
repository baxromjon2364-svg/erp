from django.shortcuts import render
from .models import Category, Product, Sale, SaleItem, User
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategorySerializer, ProductSerializer, SaleItemSerializer, SaleSerializer, UserSerializer
from django.db import transaction
from rest_framework.exceptions import ValidationError
from .permissions import IsCashierUserOnly,IsAdminUserOnly
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum,F


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer




class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    def get_queryset(self):
        return Product.objects.filter(stock_quantity__gt=0)





class SaleItemViewSet(ModelViewSet):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer

class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserOnly]

    def get(self, request):
        foyda_statikasi = SaleItem.objects.select_related('product').aggregate(
            umumiy_foyda=Sum(
                (F('price_at_sale') - F('product__purchase_price')) * F('quantity')
            ),
            umumiy_savdo_hajmi=Sum(
                F('price_at_sale') * F('quantity')
            )
        )

        return Response({
            "jami_foyda": foyda_statikasi['umumiy_foyda'] or 0,
            "jami_savdo": foyda_statikasi['umumiy_savdo_hajmi'] or 0
        })




class CheckoutAPIView2(APIView):
    permission_classes = [IsAuthenticated, IsCashierUserOnly]

    def post(self, request):
        tovarlar = request.data.get("items")
        tulov_turi = request.data.get("payment_type", "CASH")
        kassir=request.user

        try:
            with transaction.atomic():
                yangi_savdo = Sale.objects.create(
                    cashier=kassir,
                    total_amount=0,
                    payment_type=tulov_turi
                )
                jami_summa = 0

                for tovar in tovarlar:
                    mahsulot_id = tovar['product_id']
                    sotilgan_soni = tovar['quantity']

                    if sotilgan_soni <= 0:
                        raise ValidationError(f"Xato miqdor kiritdingiz! Miqdor 0 dan katta bo'lishi shart.")

                    try:
                        ombordagi_mahsulot = Product.objects.get(product_id=mahsulot_id)
                    except Product.DoesNotExist:
                        raise ValidationError(f"ID={mahsulot_id} bo'lgan mahsulot bazada topilmadi.")
                    sotilish_narxi = ombordagi_mahsulot.selling_price

                    if ombordagi_mahsulot.stock_quantity < sotilgan_soni:
                        raise ValidationError(f"{ombordagi_mahsulot.name} omborda yetarli emas qolgani : {ombordagi_mahsulot.stock_quantity}")

                    ombordagi_mahsulot.stock_quantity -= sotilgan_soni
                    ombordagi_mahsulot.save()
                    jami_summa += sotilish_narxi * sotilgan_soni

                    SaleItem.objects.create(
                        sale_id=yangi_savdo,
                        product=ombordagi_mahsulot,
                        quantity=sotilgan_soni,
                        price_at_sale=sotilish_narxi
                    )

                yangi_savdo.total_amount = jami_summa
                yangi_savdo.save()

            return Response({"message": "Sotuv muvaffaqiyatli yakunlandi"}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response("savdo tugallanmadi")