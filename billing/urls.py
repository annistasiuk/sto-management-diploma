from django.urls import path
from . import views

urlpatterns = [
    path('generate/<int:repair_id>/', views.generate_invoice_pdf_view, name='generate_invoice'),

    path('send/<int:repair_id>/', views.send_invoice_email_view, name='send_invoice'),
]