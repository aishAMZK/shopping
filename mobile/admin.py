from django.contrib import admin
from .models import Product
from .models import Customer
from .models import Order
# from .models import Category

class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price']

# Register your models here.

admin.site.register(Product, AdminProduct)
# admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)