from django.contrib import admin
from django.urls import path, include  
from rest_framework.authtoken import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.obtain_auth_token), 
    path('', include('users.urls')),  
]


