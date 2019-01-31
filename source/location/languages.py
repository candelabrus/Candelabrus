from django.utils.translation import gettext_lazy as _


class Language:
    # --- Indo-European ---
    # Germanic
    ENGLISH = 0
    GERMAN = 1
    DUTCH = 2
    DANISH = 3
    SWEDISH = 4
    ICELANDIC = 5
    NORWEGIAN = 6
    # Romance
    PORTUGUESE = 10
    SPANISH = 11
    ITALIAN = 12
    FRENCH = 13
    ROMANIAN = 14
    CATALAN = 15
    GALICIAN = 16
    # Slavic
    POLISH = 20
    UKRANIAN = 21
    RUSSIAN = 22
    BELARUSSIAN = 23
    HUNGARIAN = 24
    BULGARIAN = 25
    SERBOCROATIAN = 26
    SLOVAK = 27
    CZECH = 28
    BOSNIAN = 29
    MACEDONIAN = 30
    # Celtic
    IRISH = 35
    WELSH = 36
    # Hellenic
    GREEK = 38
    # Finnic
    FINNISH = 41
    ESTONIAN = 42
    SAMI = 43
    # Baltic
    LITHUANIAN = 45
    LATVIAN = 46
    # From unicorns and fairy dust
    ALBANIAN = 50
    BASQUE = 51

    CHOICES = (
        (ENGLISH, _('English')),
        (GERMAN, _('German')),
        (DUTCH, _('Dutch')),
        (DANISH, _('Danish')),
        (SWEDISH, _('Swedish')),
        (ICELANDIC, _('Icelandic')),
        (NORWEGIAN, _('Norwegian')),
        (PORTUGUESE, _('Portuguese')),
        (SPANISH, _('Spanish')),
        (ITALIAN, _('Italian')),
        (FRENCH, _('French')),
        (ROMANIAN, _('Romanian')),
        (CATALAN, _('Catalan')),
        (GALICIAN, _('Galician')),
        (POLISH, _('Polish')),
        (UKRANIAN, _('Ukrainian')),
        (RUSSIAN, _('Russian')),
        (BELARUSSIAN, _('Belarussian')),
        (HUNGARIAN, _('Hungarian')),
        (BULGARIAN, _('Bulgarian')),
        (SERBOCROATIAN, _('Serbo-Croatian')),
        (SLOVAK, _('Slovak')),
        (CZECH, _('Czech')),
        (BOSNIAN, _('Bosnian')),
        (MACEDONIAN, _('Macedonian')),
        (IRISH, _('Irish')),
        (WELSH, _('Welsh')),
        (GREEK, _('Greek')),
        (FINNISH, _('Finnish')),
        (ESTONIAN, _('Estonian')),
        (SAMI, _('Sami')),
        (LITHUANIAN, _('Lithuanian')),
        (LATVIAN, _('Latvian')),
        (ALBANIAN, _('Albanian')),
        (BASQUE, _('Basque')),
    )
