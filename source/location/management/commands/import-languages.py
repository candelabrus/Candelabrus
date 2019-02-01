import os
import csv
from django.core.management.base import BaseCommand
from location import models as location


class Command(BaseCommand):
    help = 'Creates ISO 639 language database from a csv file'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **options):
        file = options['file'][0]

        if not os.path.isfile(file):
            print("Bad file path.")
            exit(-1)

        with open(file) as file:
            reader = csv.reader(file)
            next(reader)
            for a3, a2, name in reader:
                if not location.Language.objects.filter(alpha2=a2).exists():
                    location.Language(name=name, alpha2=a2, alpha3=a3).save()
