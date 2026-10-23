from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator

class Component(models.Model):
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    component = models.ForeignKey(Component, on_delete=models.PROTECT, related_name='orders')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f'Order #{self.pk} - {self.component.name}'

class Inventory(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name='inventory_records')
    quantity_change = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, blank=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return f'{self.component.name}: {self.quantity_change}'
