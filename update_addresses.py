#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from areas.models import ServiceArea

def update_all_addresses():
    """Update all service areas to use the standard address"""
    
    # Standard address for all locations
    standard_address = "3380 Eglinton Ave E\nUnit 906, Toronto, ON"
    
    print("Updating all service area addresses...")
    
    # Get all service areas
    service_areas = ServiceArea.objects.all()
    
    updated_count = 0
    for area in service_areas:
        # Update the address
        area.address = standard_address
        area.save()
        updated_count += 1
        print(f"Updated {area.name}: {standard_address}")
    
    print(f"\nSummary:")
    print(f"Updated {updated_count} service areas")
    print(f"All locations now use the standard address: {standard_address}")

if __name__ == '__main__':
    update_all_addresses()
