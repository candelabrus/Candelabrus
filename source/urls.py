from django.contrib import admin
from django.urls import path, include
from candelabrus import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('markdownx/', include('markdownx.urls')),
    path('admin/', admin.site.urls),
    path('fo/', include('fons.urls')),
    path('dj/', include('dejure.urls')),
    path('dw/', include('darwin.urls')),
    path('nz/', include('nietz.urls')),
    path('mk/', include('mereokratos.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
