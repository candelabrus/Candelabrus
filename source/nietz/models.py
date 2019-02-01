from django.db import models as djm
from django.contrib.postgres import fields as pg
from markdownx.models import MarkdownxField

from location import models as location


def fallacy_pic_path(fallacy, filename):
    return f'nz/i/{fallacy.name.replace(" ", "_")}.{filename.split(".")[-1]}'


class Fallacy(djm.Model):
    # Language agnostic identifier (usually latin or english)
    name = djm.CharField(max_length=50, unique=True)
    # Fallacy variants point to their generalizations
    parent = djm.ForeignKey('self', on_delete=djm.PROTECT, null=True, blank=True)
    # A cover image
    image = djm.ImageField(upload_to=fallacy_pic_path, null=True, blank=True)
    related = djm.ManyToManyField('self', blank=True)
    categories = djm.ManyToManyField('FallacyCategory', blank=True)

    def __str__(self):
        if self.parent is None:
            return self.name
        else:
            return f"{self.name} ({self.parent.name})"

    class Meta:
        verbose_name_plural = 'fallacies'
        ordering = ['name']


class LocalizedFallacy(djm.Model):
    fallacy = djm.ForeignKey(Fallacy, on_delete=djm.PROTECT)
    language = djm.ForeignKey(location.Language, on_delete=djm.PROTECT)
    name = djm.CharField(max_length=50)  # Fallacy name in this locale
    description = MarkdownxField()  # Description in this locale
    exceptions = MarkdownxField(null=True, blank=True)  # Exceptions in this locale
    sources = pg.ArrayField(djm.URLField(), null=True, blank=True)  # Array with external references to this fallacy

    def __str__(self):
        return f'{self.name} - {self.fallacy.name} ({self.language})'

    class Meta:
        verbose_name_plural = 'localized fallacies'
        unique_together = [('fallacy', 'language'), ('name', 'language')]
        ordering = ['name']


class FallacyExample(djm.Model):
    parent = djm.ForeignKey(LocalizedFallacy, on_delete=djm.PROTECT)
    content = MarkdownxField()
    explanation = MarkdownxField()

    class Meta:
        unique_together = ['parent', 'content']


class FallacyCategory(djm.Model):
    name = djm.CharField(max_length=20)
    color = djm.CharField(max_length=6)
