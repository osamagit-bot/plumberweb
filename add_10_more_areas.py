import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from areas.models import ServiceArea

# Add 10 more Canadian service areas
more_areas = [
    {
        'name': 'Scarborough',
        'slug': 'scarborough',
        'phone': '(416) 123-4567',
        'email': 'scarborough@plumberondemand.ca',
        'address': '1234 Kingston Road, Scarborough, ON M1N 1C4',
    },
    {
        'name': 'North York',
        'slug': 'north-york',
        'phone': '(416) 234-5678',
        'email': 'northyork@plumberondemand.ca',
        'address': '5678 Yonge Street, North York, ON M2N 5S2',
    },
    {
        'name': 'Etobicoke',
        'slug': 'etobicoke',
        'phone': '(416) 345-6789',
        'email': 'etobicoke@plumberondemand.ca',
        'address': '9012 Islington Avenue, Etobicoke, ON M9A 3N4',
    },
    {
        'name': 'Ajax',
        'slug': 'ajax',
        'phone': '(905) 456-7890',
        'email': 'ajax@plumberondemand.ca',
        'address': '3456 Harwood Avenue, Ajax, ON L1S 2H6',
    },
    {
        'name': 'Pickering',
        'slug': 'pickering',
        'phone': '(905) 567-8901',
        'email': 'pickering@plumberondemand.ca',
        'address': '7890 Kingston Road, Pickering, ON L1V 1A7',
    },
    {
        'name': 'Whitby',
        'slug': 'whitby',
        'phone': '(905) 678-9012',
        'email': 'whitby@plumberondemand.ca',
        'address': '2345 Dundas Street, Whitby, ON L1N 2L3',
    },
    {
        'name': 'Oshawa',
        'slug': 'oshawa',
        'phone': '(905) 789-0123',
        'email': 'oshawa@plumberondemand.ca',
        'address': '6789 King Street, Oshawa, ON L1H 1G8',
    },
    {
        'name': 'Milton',
        'slug': 'milton',
        'phone': '(905) 890-1234',
        'email': 'milton@plumberondemand.ca',
        'address': '1357 Main Street, Milton, ON L9T 2R4',
    },
    {
        'name': 'Georgetown',
        'slug': 'georgetown',
        'phone': '(905) 901-2345',
        'email': 'georgetown@plumberondemand.ca',
        'address': '2468 Guelph Street, Georgetown, ON L7G 4A1',
    },
    {
        'name': 'Aurora',
        'slug': 'aurora',
        'phone': '(905) 012-3456',
        'email': 'aurora@plumberondemand.ca',
        'address': '3579 Yonge Street, Aurora, ON L4G 1L8',
    }
]

for area_data in more_areas:
    area, created = ServiceArea.objects.get_or_create(
        slug=area_data['slug'],
        defaults=area_data
    )
    if created:
        print(f"Created service area: {area.name}")
    else:
        print(f"Service area already exists: {area.name}")

print("10 more Canadian service areas added!")