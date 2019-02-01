from django.utils import translation
from django.shortcuts import render

from nietz import models as m


def index(request):
    return render(request, 'nietz/index.html', None)


def fallacies(request):
    localized_fallacies = m.LocalizedFallacy.objects.filter(language__alpha2=translation.get_language())
    untranslated_fallacies = m.LocalizedFallacy.objects \
        .filter(language__alpha2='en', fallacy__parent=None) \
        .exclude(fallacy__localizedfallacy__language__alpha2=translation.get_language())

    context = {'fallacies': localized_fallacies,
               'full_translation': len(untranslated_fallacies) == 0,
               'untranslated_fallacies': untranslated_fallacies}
    return render(request, 'nietz/fallacies.html', context)
