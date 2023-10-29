from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from dashboards.views import IndexView, DocumentationView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('doc/<str:doc>', DocumentationView.as_view(), name='documentation'),
    path('doc/', DocumentationView.as_view(), name='documentation'),

    path('admin/', admin.site.urls),
    path('dashboard/', include("dashboards.urls")),
    path('sap/', include("sap_data.urls")),
    path('account/', include("account.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
