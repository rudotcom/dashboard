from django.urls import path

from dashboards.views import *

app_name = "dashboard"
urlpatterns = [
    path('analytics/', DashboardAnalyticsView.as_view(), name='analytics'),
    path('crm/', DashboardCRMView.as_view(), name='crm'),
    path('ecommerce/', DashboardECommerceView.as_view(), name='ecommerce'),
    path('logistic/', DashboardLogisticView.as_view(), name='logistic'),
    path('academy/', DashboardAcademyView.as_view(), name='academy'),
    path('faq/', DashboardFAQView.as_view(), name='faq'),

    path('data-list/<str:data>/', DataListView.as_view(), name='data-list'),
    path('data-create/<str:data>/<int:pk>/', DataCreateView.as_view(), name='data-create'),
    path('data-create/<str:data>/', DataCreateView.as_view(), name='data-create'),
    path('data-detail/<str:data>/<int:pk>/', DataDetailView.as_view(), name='data-detail'),
    path('data-detail/<str:data>/<int:pk>/edit', DataObjectEditView.as_view(), name='data-edit'),
    path('data-detail/<str:data>/<int:pk>/delete', DataObjectDeleteView.as_view(), name='data-delete'),
    path('data-chart/<int:pk>/add-to-dashboard', DashboardCreateView.as_view(), name='create-dashboard'),

    path('main/', DashboardMVPView.as_view(), name='main'),

    path('not-implemented', NotImplementedView.as_view(), name='not-implemented'),
]
