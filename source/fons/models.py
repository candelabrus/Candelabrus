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
    parent = djm.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='children',
        verbose_name=_('parents'),
        blank=True)
    homepage = djm.URLField(null=True, blank=True, verbose_name=_('homepage'))
    governmental = djm.BooleanField(null=True, blank=True, verbose_name=_('governmental'))

    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.title

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

    def __str__(self):
        return self.flaw

    class Meta:
        verbose_name = _('source flaw')
        verbose_name_plural = _('source flaws')


class Citation(djm.Model):
    source = djm.ForeignKey(Source, on_delete=djm.CASCADE, verbose_name=_('source'))
    content = djm.TextField(verbose_name=_('content'))  # The content which is relevant in this source
    author = djm.CharField(max_length=128, verbose_name=_('author'))

    def __str__(self):
        return f"Citation of {self.source}"

    class Meta:
        verbose_name = _('citation')
        verbose_name_plural = _('citations')


class Subject(mptt.MPTTModel):
    name = djm.CharField(max_length=32, verbose_name=_('name'))  # Default english name
    parent = mptt.TreeForeignKey('self', on_delete=djm.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('subject')
        verbose_name_plural = _('subjects')
        unique_together = (('name', 'parent'),)


class LocalizedSubject(djm.Model):
    subject = djm.ForeignKey(Subject, on_delete=djm.CASCADE, verbose_name=_('subject'), related_name='localizations')
    language = djm.ForeignKey(
        location.Language,
        on_delete=djm.PROTECT,
        verbose_name=_('language'),
        related_name='localized_subjects')
    name = djm.CharField(max_length=32, verbose_name=_('name'))
    description = djm.TextField(verbose_name=_('description'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('subject translation')
        verbose_name_plural = _('subject translations')
        unique_together = (('subject', 'language'),)


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
    subjects = djm.ManyToManyField(
        Subject,
        through='EventSubjects',
        related_name='events',
        verbose_name=_('events'))

    def __str__(self):
        return f"Event from {self.start} to {self.end}"

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')


class EventSubjects(djm.Model):
    event = djm.ForeignKey(Event, on_delete=djm.CASCADE, verbose_name=_('event'))
    subject = djm.ForeignKey(Subject, on_delete=djm.PROTECT, verbose_name=_('subject'))
    generalization = djm.IntegerField(default=0, verbose_name=_('generalization'))

    def __str__(self):
        return f"{self.event} to {self.subject}"

    class Meta:
        verbose_name = _('event subject')
        verbose_name_plural = _('event subjects')
        unique_together = (('event', 'subject'),)


class EventDivisions(djm.Model):
    event = djm.ForeignKey(Event, on_delete=djm.CASCADE, verbose_name=_('event'))
    division = djm.ForeignKey(location.Division, on_delete=djm.PROTECT, verbose_name=_('territorial division'))
    generalization = djm.IntegerField(default=0, verbose_name=_('generalization'))

    def __str__(self):
        return f"{self.event} to {self.division}"

    class Meta:
        verbose_name = _('event division')
        verbose_name_plural = _('event divisions')
        unique_together = (('event', 'division'),)


class LocalizedEvent(djm.Model):
    event = djm.ForeignKey(Event, on_delete=djm.CASCADE, verbose_name=_('event'))
    language = djm.ForeignKey(location.Language, on_delete=djm.CASCADE, verbose_name=_('language'))
    title = djm.CharField(max_length=256, verbose_name=_('title'))
    description = djm.TextField(verbose_name=_('description'))

    def __str__(self):
        return f"{self.title} ({self.language})"

    class Meta:
        verbose_name = _('event translation')
        verbose_name_plural = _('event translations')
        unique_together = (('event', 'language'),)
