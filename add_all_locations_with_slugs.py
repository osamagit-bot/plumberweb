#!/usr/bin/env python
import os
import sys
import django
from django.utils.text import slugify

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from areas.models import ServiceArea

def add_all_locations():
    # All locations provided by user
    locations = [
        "ACTON", "AJAX-PICKERING", "AURORA", "BARRIE", "BRANTFORD", "BRAMPTON",
        "BURLINGTON", "CAMBRIDGE", "ETOBICOKE", "GEORGETOWN", "GRIMSBY", "GUELPH",
        "HALTON HILLS", "HAMILTON", "INNISFIL", "KING CITY", "MARKHAM", "MILTON",
        "MISSISSAUGA", "NEWMARKET", "NIAGARA REGION", "NOBLETON", "NORTH YORK",
        "OAKVILLE", "ORANGEVILLE", "RICHMOND HILL", "SCARBOROUGH", "ST. CATHARINES",
        "STONEY CREEK", "STOUFFVILLE", "THORNHILL", "THOROLD", "TORONTO",
        "TORONTO DOWNTOWN", "TORONTO EAST", "TORONTO EAST YORK", "TORONTO MIDTOWN",
        "TORONTO UPTOWN", "TORONTO WEST", "TORONTO YORK", "VAUGHAN", "WHITBY-OSHAWA"
    ]
    
    # Base data for each location
    base_data = {
        'phone': '+14168888888',  # Default phone number
        'email': 'service@sproplumbing.com',
        'address': '3380 Eglinton Ave E\nUnit 906, Toronto, ON',
        'province': 'Ontario',
        'postal_code': 'M3C 1N5',
        'is_active': True
    }
    
    created_count = 0
    
    for location_name in locations:
        # Check if location already exists
        if ServiceArea.objects.filter(name__iexact=location_name).exists():
            print(f"Location {location_name} already exists, skipping...")
            continue
        
        # Create the service area
        area_data = base_data.copy()
        area_data['name'] = location_name
        area_data['city'] = location_name
        
        area = ServiceArea.objects.create(**area_data)
        created_count += 1
        print(f"Created: {location_name} (ID: {area.id})")
    
    print(f"\nSummary:")
    print(f"Created {created_count} new locations")
    print(f"Total locations in database: {ServiceArea.objects.count()}")

if __name__ == '__main__':
    add_all_locations()
