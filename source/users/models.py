from django.db import models as djm
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from location import models as location


class User(AbstractUser):
    name = djm.CharField(verbose_name=_('name'), null=True, max_length=256)
    gender = djm.IntegerField(
        verbose_name=_('gender'),
        choices=(
            (0, _('male')),
            (1, _('female'))),
        null=True,
        blank=True)
    language = djm.ForeignKey(
        location.Language,
        verbose_name=_('language'),
        on_delete=djm.PROTECT,
        null=True)
    location = djm.ForeignKey(
        location.Division,
        verbose_name=_('location'),
        on_delete=djm.SET_NULL,
        null=True,
        blank=True)
