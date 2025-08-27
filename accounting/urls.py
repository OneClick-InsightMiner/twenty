from django.urls import path

from .views import accounting_va_dashboard

urlpatterns = [
    path('accounting/va/', accounting_va_dashboard, name='accounting_va_dashboard'),
]
