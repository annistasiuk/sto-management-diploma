from django.urls import path
from . import views

urlpatterns = [
    path('', views.client_list_view, name='client_list'),
    path('<int:client_id>/', views.client_detail_view, name='client_detail'),
    path('<int:client_id>/edit/', views.edit_client_view, name='edit_client'),
    path('<int:client_id>/delete/', views.delete_client_view, name='delete_client'),
]