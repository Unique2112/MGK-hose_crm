from django.contrib import admin
from django.urls import path
from crm_app import views 
urlpatterns = [
    path('print-proforma/<int:pk>/', views.print_proforma, name='print_proforma'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
]
