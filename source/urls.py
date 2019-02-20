from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from candelabrus import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('markdownx/', include('markdownx.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path('fons/', include('fons.urls')),
    path('dejure/', include('dejure.urls')),
    path('darwin/', include('darwin.urls')),
    path('nietz/', include('nietz.urls')),
    path('mereokratos/', include('mereokratos.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
