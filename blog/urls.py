from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,CategoryViewSet,ProductViewSet,SaleViewSet,SaleItemViewSet,DashboardAPIView,CheckoutAPIView2

router=DefaultRouter()
router.register('product',ProductViewSet, basename='product')
router.register('user',UserViewSet, basename='user')
router.register('category',CategoryViewSet, basename='category')
router.register('sale',SaleViewSet,basename='sale')
router.register('sale_item',SaleItemViewSet, basename='sale_item')




urlpatterns=[
    path('check',CheckoutAPIView2.as_view(),name='check'),
    path('dash/',DashboardAPIView.as_view(),name='dash'),
    path('',include(router.urls)),
]
