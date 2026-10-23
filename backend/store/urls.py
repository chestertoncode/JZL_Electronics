from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, MeView, ComponentViewSet, OrderViewSet, InventoryViewSet

router = DefaultRouter()
router.register('products', ComponentViewSet, basename='product')
router.register('orders', OrderViewSet, basename='order')
router.register('inventory', InventoryViewSet, basename='inventory')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/me/', MeView.as_view(), name='me'),
    path('', include(router.urls)),
]
