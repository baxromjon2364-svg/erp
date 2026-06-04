from django.contrib import admin
from .models import Category,Product,User,SaleItem,Sale
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(User)
admin.site.register(Sale)
admin.site.register(SaleItem)
