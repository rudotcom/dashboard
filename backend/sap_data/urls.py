from django.urls import path

from sap_data.views import *

app_name = "sap_data"
urlpatterns = [
    path('lux/', LuxTableUploadView.as_view(), name='lux_table'),
    path('main/', MainView.as_view(), name='main'),
    path('month/', MonthView.as_view(), name='month'),
    path('manager/', ManagerView.as_view(), name='manager'),
    path('customer/', CustomerView.as_view(), name='customer'),
    path('compare/', CompareView.as_view(), name='compare'),
]
