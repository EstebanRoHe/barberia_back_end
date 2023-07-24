from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import BasePermission
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializer import UserSerializer, UserEmailUsernameSerializer

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
    
class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'user'
    
class IsUserOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'user' or request.user.role == 'admin')
    
class IsOwnerOrAdmin(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff

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
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
 
   
class UserUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsUserOrAdmin]
    authentication_classes = [TokenAuthentication]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        user = self.get_object()
        role = self.request.data.get('role', user.role) if self.request.user.is_staff else user.role
        serializer.save(role=role)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == request.user or request.user.role == 'admin':
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No tienes permisos necesarios"}, status=status.HTTP_403_FORBIDDEN)

    def handle_no_permission(self):
        return Response({"detail": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        

class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsUserOrAdmin]
    authentication_classes = [TokenAuthentication]
    lookup_field = 'pk' 
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == request.user or request.user.role == 'admin':
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No tienes permisos necesarios"}, status=status.HTTP_403_FORBIDDEN)

    def handle_no_permission(self):
        return Response({"detail": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    
   
class UserSearchView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        first_name = self.request.query_params.get('first_name', None)
        if first_name is not None:
            queryset = CustomUser.objects.filter(Q(first_name__icontains=first_name))
        else:
            queryset = CustomUser.objects.all()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if not serializer.data: 
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDeleteView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    authentication_classes = [TokenAuthentication]
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            self.perform_destroy(instance)
            return Response({"detail": "Usuario eliminado correctamente"},status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

class UserEmailUsernameView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserEmailUsernameSerializer



