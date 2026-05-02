from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.repair_list_view, name='repair_list'),
    path('add/', views.add_repair_view, name='add_repair'),
    path('add-for-car/<int:car_id>/', views.add_repair_for_car_view, name='add_repair_for_car'),
    path('<int:repair_id>/edit/', views.edit_repair_view, name='edit_repair'),
    path('<int:repair_id>/pdf/', views.repair_pdf_view, name='repair_pdf'),
]