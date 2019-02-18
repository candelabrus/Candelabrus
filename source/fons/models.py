from django.contrib.gis.db import models as gis
from django.core.exceptions import ValidationError
from django.db import models as djm
from django.utils.translation import gettext_lazy as _
from mptt import models as mptt

from location import models as location
from nietz import models as nietz


class SourceProvider(djm.Model):
    """
    A source provider is an entity that collects information.
    Examples are public institutions, newspapers, blogs, encyclopedias.
    Providers can have both owners and sub-providers.
    Usually a governments, media corps., foundations, ... have subdivisions which are publishers on their own.
    """
    name = djm.CharField(max_length=128)
    country = djm.ForeignKey(
        location.Territory,
        on_delete=djm.SET_NULL,
        null=True, blank=True,
        verbose_name=_('country'))
    owners = djm.ManyToManyField('self', symmetrical=False, related_name='children', verbose_name=_('owners'))
    homepage = djm.URLField(null=True, blank=True, verbose_name=_('homepage'))
    governmental = djm.BooleanField(null=True, blank=True, verbose_name=_('governmental'))

    class Meta:
        verbose_name = _('source provider')
        verbose_name_plural = _('source providers')


class Source(djm.Model):
    """
    A publication which contains relevant information and can be scrutinized and eventually used to source content.
    """
    title = djm.CharField(max_length=256, verbose_name=_('title'))
    language = djm.ForeignKey(location.Language, on_delete=djm.PROTECT, verbose_name=_('language'))
    description = djm.TextField(verbose_name=_('description'))  # In the source language
    url = djm.URLField(null=True, blank=True, verbose_name=_('address'))  # When has an online resource
    provider = djm.ForeignKey(SourceProvider, on_delete=djm.PROTECT, verbose_name=_('provider'))

    class Meta:
        verbose_name = _('source')
        verbose_name_plural = _('sources')


def webpage_screenshot_img_path(webpage, filename):
    return f'fo/webpage/{webpage.id}/screenshot.{filename.split(".")[-1]}'


class Webpage(Source):
    """
    Online page source.
    """
    screenshot = djm.ImageField(
        null=True, blank=True,
        upload_to=webpage_screenshot_img_path,
        verbose_name=_('screenshot'))
    paywalled = djm.BooleanField(null=True, verbose_name=_('paywalled'))
    code = djm.TextField(null=True, blank=True, verbose_name=_('source code'))  # Web page source code

    class Meta:
        verbose_name = _('webpage')
        verbose_name_plural = _('webpages')


class Media(Source):
    """
    A media based type of source (books, songs, scientific documents).
    """
    isbn = djm.CharField(max_length=20, null=True, blank=True, unique=True)
    ismn = djm.CharField(max_length=20, null=True, blank=True, unique=True)
    isan = djm.CharField(max_length=20, null=True, blank=True, unique=True)

    # TODO Would it be to legal to include the following?:
    # cover = djm.ImageField(
    #     null=True, blank=True,
    #     upload_to=...)
    # musicbrainz = djm.URLField(null=True, blank=True)  # Musicbrainz page

    def clean(self):
        super(Media, self).clean()
        non_null = 0
        if self.isbn is not None:
            non_null = 1
        if self.ismn is not None:
            non_null += 1
        if self.isan is not None:
            non_null += 1
        if non_null != 1:
            raise ValidationError('A media source needs a single identifier.')

    class Meta:
        verbose_name = _('media')
        verbose_name_plural = _('medias')


class SourceFlaw(djm.Model):
    """
    A flaw associated with a Source.
    """
    source = djm.ForeignKey(Source, on_delete=djm.CASCADE, verbose_name=_('source'))
    flaw = djm.CharField(
        max_length=32,
        choices=(
            ('false', _('false')),  # Contains information that is demonstrably false
            ('tampered', _('tampered')),  # Distorting the information
            ('speculative', _('speculative')),  # Based on either past or future speculations
            ('partial', _('partial')),  # Showing only one side of what's presented
            ('generalization', _('generalization')),  # Generalizing what's true for a few
            ('unfounded', _('unfounded'))),  # Claiming without presenting enough evidence
        null=True, blank=True,
        verbose_name=_('flaw'))
    fallacy = djm.ForeignKey(
        nietz.Fallacy,
        on_delete=djm.PROTECT,
        null=True, blank=True,
        verbose_name=_('fallacy'))
    # Justification in the same language the source is written in
    justification = djm.TextField(verbose_name=_('justification'))
    verified = djm.BooleanField(default=False, verbose_name=_('verified'))

    class Meta:
        verbose_name = _('source flaw')
        verbose_name_plural = _('source flaws')


class Citation(djm.Model):
    source = djm.ForeignKey(Source, on_delete=djm.CASCADE, verbose_name=_('source'))
    content = djm.TextField(verbose_name=_('content'))  # The content which is relevant in this source
    author = djm.CharField(max_length=128, verbose_name=_('author'))

    class Meta:
        verbose_name = _('citation')
        verbose_name_plural = _('citations')


class Area(mptt.MPTTModel):
    name = djm.CharField(max_length=32, verbose_name=_('name'))  # Default english name
    parent = mptt.TreeForeignKey('self', on_delete=djm.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('area')
        verbose_name_plural = _('areas')
        unique_together = (('name', 'parent'),)


class LocalizedArea(djm.Model):
    area = djm.ForeignKey(Area, on_delete=djm.CASCADE, verbose_name=_('area'), related_name='localizations')
    language = djm.ForeignKey(
        location.Language,
        on_delete=djm.PROTECT,
        verbose_name=_('language'),
        related_name='localized_areas')
    name = djm.CharField(max_length=32, verbose_name=_('name'))
    description = djm.TextField(verbose_name=_('description'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('area translation')
        verbose_name_plural = _('area translations')
        unique_together = (('area', 'language'),)


class Event(djm.Model):
    start = djm.DateTimeField(verbose_name=_('initial time'))
    end = djm.DateTimeField(null=True, blank=True, verbose_name=_('final time'))
    children = djm.ManyToManyField('self', symmetrical=False, verbose_name=_('children'))
    source_citations = djm.ManyToManyField(Citation, verbose_name=_('source citations'))
    divisions = djm.ManyToManyField(
        location.Division,
        through='EventDivisions',
        related_name='events',
        verbose_name=_('territorial divisions'))
    location = gis.PointField(geography=True, null=True, blank=True, verbose_name=_('location'))
    areas = djm.ManyToManyField(
        Area,
        through='EventAreas',
        related_name='events',
        verbose_name=_('areas'))

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')


class EventAreas(djm.Model):
    event = djm.ForeignKey(Event, on_delete=djm.CASCADE, verbose_name=_('event'))
    area = djm.ForeignKey(Area, on_delete=djm.PROTECT, verbose_name=_('area'))
    generalization = djm.IntegerField(default=0, verbose_name=_('generalization'))

    class Meta:
        verbose_name = _('event area')
        verbose_name_plural = _('event areas')
        unique_together = (('event', 'area'),)


class EventDivisions(djm.Model):
    event = djm.ForeignKey(Event, on_delete=djm.CASCADE, verbose_name=_('event'))
    division = djm.ForeignKey(location.Division, on_delete=djm.PROTECT, verbose_name=_('territorial division'))
    generalization = djm.IntegerField(default=0, verbose_name=_('generalization'))

    class Meta:
        verbose_name = _('event division')
        verbose_name_plural = _('event divisions')
        unique_together = (('event', 'division'),)


class LocalizedEvent(djm.Model):
    event = djm.ForeignKey(Event, on_delete=djm.CASCADE, verbose_name=_('event'))
    language = djm.ForeignKey(location.Language, on_delete=djm.CASCADE, verbose_name=_('language'))
    title = djm.CharField(max_length=256, verbose_name=_('title'))
    description = djm.TextField(verbose_name=_('description'))

    class Meta:
        verbose_name = _('localized event')
        verbose_name_plural = _('localized events')
        unique_together = (('event', 'language'),)
