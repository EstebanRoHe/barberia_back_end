from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import BasePermission
from django.db.models import Q
from .models import CustomUser
from .serializer import UserSerializer


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
            password = self.request.data['password']
            hashed_password = make_password(password)
            serializer.save(password=hashed_password, role='user')

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    authentication_classes = [TokenAuthentication]
    
    
class UserUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [TokenAuthentication]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        user = self.get_object()
        role = self.request.data.get('role', user.role) if self.request.user.is_staff else user.role
        serializer.save(role=role)
        
class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    authentication_classes = [TokenAuthentication]
    lookup_field = 'pk' 
    
class UserSearchView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        first_name = self.request.query_params.get('first_name', None)
        if first_name is not None:
            #Q espara realizar una búsqueda insensible a mayúsculas y minúsculas
            queryset = CustomUser.objects.filter(Q(first_name__icontains=first_name))
        else:
            queryset = CustomUser.objects.all()
        return queryset

class UserDeleteView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    authentication_classes = [TokenAuthentication]
    lookup_field = 'pk'
   


