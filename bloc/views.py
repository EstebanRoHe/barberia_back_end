from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from .models import Bloc
from .serializer import BlocSerializer
from users.views import IsAdmin, IsUserOrAdmin, IsUser
from rest_framework.exceptions import PermissionDenied

class CreateBlocView(generics.CreateAPIView):
    queryset = Bloc.objects.all()
    serializer_class = BlocSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsUserOrAdmin]

    def perform_create(self, serializer):
        user_id = self.request.data.get('user')
        authenticated_user_id = self.request.user.id

        if user_id and int(user_id) == authenticated_user_id:
            serializer.save(user_id=user_id)
        elif user_id is None:
            serializer.save(user_id=authenticated_user_id)
        else:  
            raise PermissionDenied(detail="No tienes permisos necesarios")  
                      
class BlocListView(generics.ListCreateAPIView):
    queryset = Bloc.objects.all()
    serializer_class = BlocSerializer
    
    
class UpdateBlocView(generics.RetrieveUpdateAPIView):
    queryset = Bloc.objects.all()
    serializer_class = BlocSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsUserOrAdmin]
    lookup_field = 'pk'
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No tienes permisos necesarios"}, status=status.HTTP_403_FORBIDDEN)

    def handle_no_permission(self):
        return Response({"detail": "Bloc no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
    
class FindByIdBlocView(generics.RetrieveAPIView):
    queryset = Bloc.objects.all()
    serializer_class = BlocSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsUserOrAdmin]
    lookup_field = 'pk' 
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def handle_no_permission(self):
        return Response({"detail": "Bloc no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    
class DeleteBlocView(generics.DestroyAPIView):
    queryset = Bloc.objects.all()
    serializer_class = BlocSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsUserOrAdmin] 

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user or request.user.role == 'admin':
         #if instance.user == request.user:
            self.perform_destroy(instance)
            return Response({"detail": "Bloc eliminado correctamente"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No tienes permisos necesarios"}, status=status.HTTP_403_FORBIDDEN)
    

    