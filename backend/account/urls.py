from django.urls import path

from account.views import *

app_name = "account"
urlpatterns = [
    path('', AccountView.as_view(), name='index'),
    path('notifications/', AccountNotificationsView.as_view(), name='notifications'),
    path('settings/', AccountSettingsView.as_view(), name='settings'),
]
