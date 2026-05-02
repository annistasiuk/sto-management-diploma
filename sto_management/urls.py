from django.contrib import admin
from django.urls import path, include

from sto_management.views import (
    home_view,
    update_repair_status_view,
    user_login_view,
    user_logout_view
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', user_login_view, name='login'),
    path('logout/', user_logout_view, name='logout'),

    path('cars/', include('cars.urls')),
    path('repairs/', include('repairs.urls')),
    path('billing/', include('billing.urls')),
    path('clients/', include('clients.urls')),

    path('', home_view, name='home'),

    path(
        'repair/<int:repair_id>/status/<str:status>/',
        update_repair_status_view,
        name='update_repair_status'
    ),
]