#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from areas.models import ServiceArea

def create_locations():
    """Create service area locations"""
    
    locations = [
        'ACTON', 'AJAX-PICKERING', 'AURORA', 'BARRIE', 'BRANTFORD', 'BRAMPTON',
        'BURLINGTON', 'CAMBRIDGE', 'ETOBICOKE', 'GEORGETOWN', 'GRIMSBY', 'GUELPH',
        'HALTON HILLS', 'HAMILTON', 'INNISFIL', 'KING CITY', 'MARKHAM', 'MILTON',
        'MISSISSAUGA', 'NEWMARKET', 'NIAGARA REGION', 'NOBLETON', 'NORTH YORK',
        'OAKVILLE', 'ORANGEVILLE', 'RICHMOND HILL', 'SCARBOROUGH', 'ST. CATHARINES',
        'STONEY CREEK', 'STOUFFVILLE', 'THORNHILL', 'THOROLD', 'TORONTO',
        'TORONTO DOWNTOWN', 'TORONTO EAST', 'TORONTO EAST YORK', 'TORONTO MIDTOWN',
        'TORONTO UPTOWN', 'TORONTO WEST', 'TORONTO YORK', 'VAUGHAN', 'WHITBY-OSHAWA'
    ]
    
    created_count = 0
    
    for location in locations:
        area, created = ServiceArea.objects.get_or_create(
            name=location,
            defaults={
                'phone': '+14165550100',
                'email': f'service.{location.lower().replace(" ", "").replace("-", "")}@sproplumbing.com',
                'address': f'Service Area: {location}',
                'city': 'Toronto' if 'TORONTO' in location else location.split()[0].title(),
                'province': 'Ontario',
            }
        )
        
        if created:
            created_count += 1
            print(f"✓ Created location: {area.name}")
        else:
            print(f"- Location already exists: {area.name}")
    
    print(f"\nSummary: {created_count} new locations created out of {len(locations)} total locations.")

if __name__ == '__main__':
    print("Creating service area locations...")
    create_locations()
    print("Done!")