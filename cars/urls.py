from django.urls import path
from . import views

urlpatterns = [
    path('', views.car_list_view, name='car_list'),
    path('<int:car_id>/', views.car_detail_view, name='car_detail'),
    path('<int:car_id>/edit/', views.edit_car_view, name='edit_car'),
    path('<int:car_id>/delete/', views.delete_car_view, name='delete_car'),
]