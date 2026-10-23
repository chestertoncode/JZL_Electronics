from django.contrib import admin
from .models import Component, Order, Inventory

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'component', 'quantity', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'component__name')

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'component', 'quantity_change', 'date_added', 'added_by')
    list_filter = ('date_added',)
