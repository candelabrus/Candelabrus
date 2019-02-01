from django.utils import translation as t
from django.shortcuts import render

from nietz import models as m


def index(request):
    return render(request, 'nietz/index.html', None)


def fallacies(request):
    localized_fallacies = m.LocalizedFallacy.objects.filter(language__alpha2=t.get_language())
    untranslated_fallacies = m.LocalizedFallacy.objects \
        .filter(language__alpha2='en', fallacy__parent=None) \
        .exclude(fallacy__localizedfallacy__language__alpha2=t.get_language())

    context = {'fallacies': localized_fallacies,
               'untranslated_fallacies': untranslated_fallacies}
    return render(request, 'nietz/fallacies.html', context)


def fallacy(request, identifier):
    translations = m.LocalizedFallacy.objects.filter(fallacy_id=identifier).all()
    languages = list(map(lambda translated_fallacy: translated_fallacy.language, translations))
    language = t.get_language()
    fallacy_obj = None
    is_translated = False
    for translated_fallacy in translations:
        if translated_fallacy.language.alpha2 == language:
            fallacy_obj = translated_fallacy
            is_translated = True
            break
        if translated_fallacy.language == 'en':
            fallacy_obj = translated_fallacy

    children = m.LocalizedFallacy.objects.filter(fallacy__parent=fallacy_obj.fallacy, language__alpha2=language)
    untranslated_children = m.LocalizedFallacy.objects \
        .filter(fallacy__parent=fallacy_obj.fallacy, language__alpha2='en') \
        .exclude(fallacy__localizedfallacy__language__alpha2=language)

    related = m.LocalizedFallacy.objects.filter(fallacy__related=fallacy_obj.fallacy, language__alpha2=language)
    untranslated_related = m.LocalizedFallacy.objects \
        .filter(fallacy__related=fallacy_obj.fallacy, language__alpha2='en') \
        .exclude(fallacy__localizedfallacy__language__alpha2=language)

    context = {'fallacy': fallacy_obj,
               'languages': languages,
               'is_translated': is_translated,
               'children': children,
               'untranslated_children': untranslated_children,
               'related': related,
               'untranslated_related': untranslated_related}
    return render(request, 'nietz/fallacy.html', context)
