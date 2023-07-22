from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from users.models import CustomUser
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from .models import Bloc
from .serializer import BlocSerializer
 
class CreateBlocView(generics.CreateAPIView):
    queryset = Bloc.objects.all()
    serializer_class = BlocSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        user_id = self.request.data.get('user')
        if user_id:
            user = get_object_or_404(CustomUser, pk=user_id)
            serializer.save(user=user)
        else:
            serializer.save()
        
class BlocListView(generics.ListCreateAPIView):
    queryset = Bloc.objects.all()
    serializer_class = BlocSerializer

class UpdateBlocView(generics.RetrieveUpdateAPIView):
    queryset = Bloc.objects.all()
    serializer_class = BlocSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class FindByIdBlocView(generics.RetrieveAPIView):
    queryset = Bloc.objects.all()
    serializer_class = BlocSerializer
    
class DeleteBlocView(generics.DestroyAPIView):
    queryset = Bloc.objects.all()
    serializer_class = BlocSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    

