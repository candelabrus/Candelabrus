from django.http import HttpResponse
from django.template import loader
from django.utils import translation


def index(request):
    translation.activate('pt')
    template = loader.get_template('candelabrus/index.html')
    return HttpResponse(template.render(None, request))
