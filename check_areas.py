#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from areas.models import ServiceArea

def check_existing_areas():
    print("Checking existing ServiceAreas:")
    areas = ServiceArea.objects.all()
    print(f"Total areas: {areas.count()}")
    
    for area in areas:
        print(f"ID: {area.id}, Name: {area.name}, City: {area.city}")

if __name__ == '__main__':
    check_existing_areas()
