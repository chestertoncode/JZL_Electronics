from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Component, Order, Inventory

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    display_name = serializers.CharField(source='first_name', required=False, allow_blank=True, max_length=100)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'display_name']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source='first_name', read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'display_name', 'is_staff']

class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ['id', 'name', 'description', 'quantity', 'price', 'image', 'created_at']
        read_only_fields = ['id', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(source='component', queryset=Component.objects.all(), write_only=True)
    product_name = serializers.CharField(source='component.name', read_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'product', 'product_name', 'quantity', 'unit_price', 'total_price', 'status', 'created_at']
        read_only_fields = ['id', 'unit_price', 'status', 'created_at', 'total_price', 'product_name']

    def validate(self, attrs):
        component = attrs['component']
        quantity = attrs['quantity']
        if quantity < 1:
            raise serializers.ValidationError({'quantity': 'Quantity must be at least 1.'})
        if component.quantity < quantity:
            raise serializers.ValidationError({'quantity': 'There is not enough stock for this order.'})
        return attrs

    def create(self, validated_data):
        from django.db import transaction
        from django.db.models import F
        component = validated_data['component']
        quantity = validated_data['quantity']
        with transaction.atomic():
            component = Component.objects.select_for_update().get(pk=component.pk)
            if component.quantity < quantity:
                raise serializers.ValidationError({'quantity': 'There is not enough stock for this order.'})
            component.quantity = F('quantity') - quantity
            component.save(update_fields=['quantity'])
            component.refresh_from_db()
            order = Order.objects.create(
                user=self.context['request'].user,
                component=component,
                quantity=quantity,
                unit_price=component.price,
            )
            Inventory.objects.create(component=component, quantity_change=-quantity, note=f'Order #{order.pk}', added_by=self.context['request'].user)
            return order

class InventorySerializer(serializers.ModelSerializer):
    component_name = serializers.CharField(source='component.name', read_only=True)
    added_by_username = serializers.CharField(source='added_by.username', read_only=True)
    class Meta:
        model = Inventory
        fields = ['id', 'component', 'component_name', 'quantity_change', 'date_added', 'note', 'added_by', 'added_by_username']
        read_only_fields = ['id', 'date_added', 'added_by']
