from django.utils import translation as t
from django.shortcuts import render
from fons import models as m


def index(request):
    return render(request, 'fons/index.html', None)


def catalog(request):
    return render(request, 'fons/catalog.html', {'nodes': m.Subject.objects.all()})


def subject(request, identifier):
    language = request.GET['l'] if 'l' in request.GET else t.get_language()
    subject = m.Subject.objects.prefetch_related('localizations__language').get(id=identifier)
    current_localization = subject.localizations.filter(language__alpha2=language).first()
    events = subject.events.order_by('start').reverse().all()[:10]

    context = {
        'subject': subject,
        'loc_subject': current_localization,
        'events': events
    }
    return render(request, 'fons/subject.html', context)
