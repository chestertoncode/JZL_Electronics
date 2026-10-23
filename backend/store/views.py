from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, viewsets
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Component, Order, Inventory
from .serializers import RegisterSerializer, UserSerializer, ComponentSerializer, OrderSerializer, InventorySerializer
from .permissions import ReadOnlyOrStaff

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data)

class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    permission_classes = [ReadOnlyOrStaff]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options']
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.select_related('component', 'user').all()
        return Order.objects.select_related('component').filter(user=self.request.user)

class InventoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Inventory.objects.select_related('component', 'added_by').all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAdminUser]
