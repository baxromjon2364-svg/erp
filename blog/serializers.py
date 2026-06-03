from rest_framework.serializers import ModelSerializer
from .models import Category,Product,Sale,SaleItem,User


class CategorySerializer(ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields='__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'


class SaleSerializer(ModelSerializer):
    class Meta:
        model=Sale
        fields='__all__'

class SaleItemSerializer(ModelSerializer):
    class Meta:
        model=SaleItem
        fields='__all__'