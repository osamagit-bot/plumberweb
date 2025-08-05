import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from areas.models import ServiceArea

# All Canadian service areas
all_areas = [
    'ACTON', 'AJAX-PICKERING', 'AURORA', 'BARRIE', 'BRANTFORD', 'BRAMPTON', 
    'BURLINGTON', 'CAMBRIDGE', 'ETOBICOKE', 'GEORGETOWN', 'GRIMSBY', 'GUELPH', 
    'HALTON HILLS', 'HAMILTON', 'INNISFIL', 'KING CITY', 'MARKHAM', 'MILTON', 
    'MISSISSAUGA', 'NEWMARKET', 'NIAGARA REGION', 'NOBLETON', 'NORTH YORK', 
    'OAKVILLE', 'ORANGEVILLE', 'RICHMOND HILL', 'SCARBOROUGH', 'ST. CATHARINES', 
    'STONEY CREEK', 'STOUFFVILLE', 'THORNHILL', 'THOROLD', 'TORONTO', 
    'TORONTO DOWNTOWN', 'TORONTO EAST', 'TORONTO EAST YORK', 'TORONTO MIDTOWN', 
    'TORONTO UPTOWN', 'TORONTO WEST', 'TORONTO YORK', 'VAUGHAN', 'WHITBY-OSHAWA'
]

for area_name in all_areas:
    slug = area_name.lower().replace(' ', '-').replace('_', '-')
    phone = f"(905) {hash(area_name) % 900 + 100}-{hash(area_name) % 9000 + 1000}"
    
    area_data = {
        'name': area_name.title(),
        'slug': slug,
        'phone': phone,
        'email': f'{slug}@plumberondemand.ca',
        'address': f'123 Main Street, {area_name.title()}, ON',
        'is_active': True
    }
    
    area, created = ServiceArea.objects.get_or_create(
        slug=slug,
        defaults=area_data
    )
    if created:
        print(f"Created: {area.name}")
    else:
        print(f"Exists: {area.name}")

print(f"\nTotal areas: {ServiceArea.objects.count()}")