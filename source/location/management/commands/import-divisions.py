import os
import csv
from django.core.management.base import BaseCommand
from location import models as location


class Command(BaseCommand):
    help = 'Creates Portuguese territorial division database'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)
        parser.add_argument('alpha2', nargs='+', type=str)

    def handle(self, *args, **options):
        file = options['file'][0]
        alpha2 = options['alpha2'][0]

        if not os.path.isfile(file):
            print("Bad file path.")
            exit(-1)

        territory = location.Territory.objects.get(alpha2=alpha2)
        with open(file) as file:
            reader = csv.reader(file)
            next(reader)
            regions = dict()
            districts = dict()
            municipalities = dict()
            for dicofre, region_name, district_name, municipality_name, parish_name, _ in reader:
                parish_name: str = parish_name.replace('união das freguesias de ', '')
                district_code = dicofre[0:2]
                municipality_code = dicofre[0:4]
                depth = 0

                # Region, exclusive to the archipelagos
                island = district_name.startswith('ilha')
                if island:
                    if region_name in regions:
                        region = regions[region_name]
                    else:
                        region = location.Division.objects.filter(
                            category=location.DivisionType.AUTONOMOUS_REGION,
                            name=region_name,
                            territory=territory,
                            depth=depth,
                            parent=None
                        ).first()
                        if region is None:
                            region = location.Division(
                                category=location.DivisionType.AUTONOMOUS_REGION,
                                name=region_name,
                                depth=depth,
                                territory=territory)
                            region.save()
                            print(f"Created autonomous region {region_name}")
                        regions[region_name] = region
                    depth += 1
                else:
                    region = None

                # District or island
                if district_code in districts:
                    district = districts[district_code]
                elif island:
                    district = location.Division.objects.filter(
                        category=location.DivisionType.ISLAND,
                        territory=territory,
                        depth=depth,
                        code=district_code,
                        parent=region
                    ).first()
                    if district is None:
                        district = location.Division(
                            category=location.DivisionType.ISLAND,
                            name=district_name,
                            code=district_code,
                            depth=depth,
                            territory=territory,
                            parent=region)
                        district.save()
                        print(f"Created island {district} in {region}")
                    districts[district_code] = district
                else:
                    district = location.Division.objects.filter(
                        category=location.DivisionType.DISTRICT,
                        territory=territory,
                        depth=depth,
                        code=district_code,
                        parent=None
                    ).first()
                    if district is None:
                        district = location.Division(
                            category=location.DivisionType.DISTRICT,
                            name=district_name,
                            code=district_code,
                            depth=depth,
                            territory=territory)
                        district.save()
                        print(f"Created district {district}")
                    districts[district_code] = district
                depth += 1

                # Municipality, always exists within districts or islands
                if municipality_code in municipalities:
                    municipality = municipalities[municipality_code]
                else:
                    municipality = location.Division.objects.filter(
                        category=location.DivisionType.MUNICIPALITY,
                        code=municipality_code,
                        depth=depth,
                        parent=district,
                        territory=territory
                    ).first()
                    if municipality is None:
                        municipality = location.Division(
                            category=location.DivisionType.MUNICIPALITY,
                            name=municipality_name,
                            code=municipality_code,
                            depth=depth,
                            parent=district,
                            territory=territory)
                        municipality.save()
                        # print(f"Created municipality {municipality}")
                    municipalities[municipality_code] = municipality
                depth += 1

                # Parish, highest division depth
                parish = location.Division.objects.filter(
                    category=location.DivisionType.PARISH,
                    code=dicofre,
                    depth=depth,
                    parent=municipality,
                    territory=territory
                ).first()
                if parish is None:
                    parish = location.Division(
                        name=parish_name,
                        code=dicofre,
                        depth=depth,
                        parent=municipality,
                        category=location.DivisionType.PARISH,
                        territory=territory)
                    parish.save()
