#!/usr/bin/env python
import os
import sys
import django
from django.utils.text import slugify

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from services.models import Service
from areas.models import ServiceArea

def populate_service_slugs():
    """Populate slugs for existing Service records"""
    services = Service.objects.filter(slug__isnull=True)
    print(f"Found {services.count()} services without slugs")
    
    for service in services:
        base_slug = slugify(service.name)
        slug = base_slug
        counter = 1
        
        # Ensure unique slug
        while Service.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        service.slug = slug
        service.save()
        print(f"Updated service '{service.name}' with slug '{slug}'")

def populate_area_slugs():
    """Populate slugs for existing ServiceArea records"""
    areas = ServiceArea.objects.filter(slug__isnull=True)
    print(f"Found {areas.count()} service areas without slugs")
    
    for area in areas:
        base_slug = slugify(area.name)
        slug = base_slug
        counter = 1
        
        # Ensure unique slug
        while ServiceArea.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        area.slug = slug
        area.save()
        print(f"Updated area '{area.name}' with slug '{slug}'")

if __name__ == "__main__":
    print("Populating slugs for existing records...")
    populate_service_slugs()
    populate_area_slugs()
    print("Done!")
