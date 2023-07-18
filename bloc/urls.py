from django.urls import path
from .views import BlocListView, CreateBlocView, UpdateBlocView, FindByIdBlocView,DeleteBlocView
urlpatterns = [
    path('list/', BlocListView.as_view(), name='bloc-list'),
    path('create/', CreateBlocView.as_view(), name='bloc-create'),
    path('update/<int:pk>/', UpdateBlocView.as_view(), name='bloc-update'),
    path('findBy/<int:pk>/', FindByIdBlocView.as_view(), name='bloc-findBy'),
    path('delete/<int:pk>/', DeleteBlocView.as_view(), name='bloc-delete'),
]