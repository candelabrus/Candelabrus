from django.urls import path
from django.utils.translation import gettext_lazy as _
from nietz import views

app_name = 'nietz'

urlpatterns = [
    path('', views.index, name='index'),
    path(_('concepts/'), views.concepts, name='concepts'),
    path(_('fallacies/'), views.fallacies, name='fallacies'),
    path(_('fallacies/<int:identifier>/'), views.fallacy, name='fallacy'),
]
