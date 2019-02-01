from django.db import models as djm
from django.contrib.gis.db import models as gis


class Language(djm.Model):
    """ISO 639 languages"""
    name = djm.CharField(max_length=30, unique=True)
    alpha2 = djm.CharField(max_length=2, unique=True)
    alpha3 = djm.CharField(max_length=3, unique=True)
    enabled = djm.BooleanField(default=False)

    def __str__(self):
        return self.name


class DivisionType:
    COUNTRY = 0
    DISTRICT = 1
    MUNICIPALITY = 2
    PARISH = 3

    CHOICES = (
        (COUNTRY, 'Country'),
        (DISTRICT, 'District'),
        (MUNICIPALITY, 'Municipality'),
        (PARISH, 'Parish'),
    )


class Territory(djm.Model):
    """
    The biggest (usually continuous) territory that a sovereign state has.
    For most states this is the whole state.
    There are states with overseas islands which own multiple territories (eg. France has France & the French Polynesia)
    """
    name = djm.CharField(max_length=60, unique=True)
    alpha2 = djm.CharField(max_length=2, unique=True)
    alpha3 = djm.CharField(max_length=3, unique=True)
    code = djm.CharField(max_length=3, unique=True)  # ISO 3166 country code
    # Government territory of non sovereign territories
    parent = djm.ForeignKey('self', on_delete=djm.CASCADE, default=None, null=True, blank=True)
    enabled = djm.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Territories'


class Division(djm.Model):
    """A division of a state territory. These are usually provinces, districts, parishes, ..."""
    territory = djm.ForeignKey(Territory, on_delete=djm.PROTECT)
    name = djm.CharField(max_length=150)  # Official local name
    abbreviation = djm.CharField(max_length=5, blank=True, null=True)  # Official name abbreviation
    code = djm.CharField(max_length=10)  # Division governmental code
    depth = djm.IntegerField()  # Subdivision depth. Lower depth divides a nation with bigger "pieces"
    coordinates = gis.PointField(geography=True, null=True, blank=True)  # Coordinate which better represents
    polygon = gis.MultiPolygonField(geography=True, null=True, blank=True)  # Geographic polygon
    category = djm.IntegerField(choices=DivisionType.CHOICES)
    parent = djm.ForeignKey('self', on_delete=djm.CASCADE, null=True, blank=True)  # Lower depth division which includes
    historical = djm.BooleanField(default=False)  # No longer exists

    def __str__(self):
        return self.name

    class Meta:
        unique_together = [('territory', 'name', 'depth', 'parent'), ('territory', 'abbreviation', 'depth')]
