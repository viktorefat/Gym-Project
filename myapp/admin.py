from django.contrib import admin
from .models import Product, Profile, CartItem, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'city', 'total_amount', 'created_at', 'is_paid')
    list_filter = ('city', 'created_at', 'is_paid')
    search_fields = ('id', 'user__username', 'first_name', 'last_name', 'phone')
    readonly_fields = ('user', 'first_name', 'last_name', 'address', 'city', 'phone', 'total_amount', 'created_at')
    inlines = [OrderItemInline]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

admin.site.register(Profile)
admin.site.register(CartItem)