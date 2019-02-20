from django.urls import path
from django.utils.translation import gettext_lazy as _

from fons import views

app_name = 'fons'

urlpatterns = [
    path('', views.index, name='index'),
    path(_('catalog'), views.catalog, name='catalog'),
    path(_('subject/<int:identifier>'), views.subject, name='subject'),
]
