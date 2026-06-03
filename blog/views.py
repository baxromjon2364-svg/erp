from django.shortcuts import render
from .models import Category, Product, Sale, SaleItem, User
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategorySerializer, ProductSerializer, SaleItemSerializer, SaleSerializer, UserSerializer



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

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
    def get(self, request):
        cache_key = "dashboard_statistika"
        statistika = cache.get(cache_key)
        if not statistika:
            jami_savdo = Sale.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
            jami_foyda = 0
            sale_items = SaleItem.objects.select_related('product').all()
            for item in sale_items:
                foyda = (item.price_at_sale - item.product.purchase_price) * item.quantity
                jami_foyda += foyda
            statistika = {
                "jami_savdo": float(jami_savdo),
                "jami_foyda": float(jami_foyda)
            }
            cache.set(cache_key, statistika, timeout=3600)
        return Response(statistika)

# {
#     "cashier_id": 1,
#     "total_amount": 125000.00,
#     "payment_type": "cash",
#     "items": [
#         {
#             "product_id": 6,
#             "quantity": 2,
#             "price_at_sale": 30000
#         },
#         {
#             "product_id": 7,
#             "quantity": 1,
#             "price_at_sale": 15000
#         }
#     ]
# }




from django.db import transaction
from django.db.models import Sum
from django.core.cache import cache



class CheckoutAPIView2(APIView):
    def post(self, request):
        tovarlar = request.data.get("items")
        jami_summa = request.data.get("total_amount")
        tulov_turi = request.data.get("payment_type", "CASH")
        kassir_id = request.data.get("cashier_id")

        if not kassir_id:
            return Response(
                {"error": "kassir ID  yuborilmadi :( "},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            yangi_savdo = Sale.objects.create(
                cashier_id=kassir_id,
                total_amount=jami_summa,
                payment_type=tulov_turi
            )

            for tovar in tovarlar:
                mahsulot_id = tovar['product_id']
                sotilgan_soni = tovar['quantity']
                sotilish_narxi = tovar['price_at_sale']

                ombordagi_mahsulot = Product.objects.get(product_id=mahsulot_id)

                if ombordagi_mahsulot.stock_quantity < sotilgan_soni:
                    raise ValueError (f"{ombordagi_mahsulot.name} omborda yetarli emas ")

                ombordagi_mahsulot.stock_quantity -= sotilgan_soni
                ombordagi_mahsulot.save()

                SaleItem.objects.create(
                    sale_id=yangi_savdo,
                    product=ombordagi_mahsulot,
                    quantity=sotilgan_soni,
                    price_at_sale=sotilish_narxi
                )

        return Response({"message": "sotuv muvaffaqiyatli yakunlandi"}, status=status.HTTP_201_CREATED)