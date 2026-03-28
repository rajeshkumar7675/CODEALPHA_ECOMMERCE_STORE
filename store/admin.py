from django.contrib import admin
from .models import Product, Cart, CartItem, Order, OrderItem

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at')
    search_fields = ('name',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')

admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
