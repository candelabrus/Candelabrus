from django.contrib import admin
from fons import models as m
from django_mptt_admin.admin import DjangoMpttAdmin


class LocalizedSubjectAdmin(admin.TabularInline):
    model = m.LocalizedSubject


class SubjectAdmin(DjangoMpttAdmin):
    inlines = [
        LocalizedSubjectAdmin,
    ]


class LocalizedEventAdmin(admin.TabularInline):
    model = m.LocalizedEvent


class EventDivisionAdmin(admin.TabularInline):
    model = m.EventDivisions


class EventSubjectsAdmin(admin.TabularInline):
    model = m.EventSubjects


class EventAdmin(admin.ModelAdmin):
    inlines = [
        LocalizedEventAdmin,
        EventDivisionAdmin,
        EventSubjectsAdmin
    ]


admin.site.register(m.Subject, SubjectAdmin)
admin.site.register(m.Event, EventAdmin)
admin.site.register(m.SourceProvider)
admin.site.register(m.Source)
admin.site.register(m.Webpage)
admin.site.register(m.Media)
admin.site.register(m.SourceFlaw)
admin.site.register(m.Citation)
