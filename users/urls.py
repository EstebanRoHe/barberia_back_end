from django.urls import path
from .views import UserRegistrationView, UserListView, UserUpdateView, UserDetailView, UserSearchView, UserDeleteView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('list/', UserListView.as_view(), name='user-list'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('findByid/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/search/', UserSearchView.as_view(), name='user-search'),  
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user-delete'),
]



