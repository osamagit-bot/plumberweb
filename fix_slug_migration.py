#!/usr/bin/env python
import os
import sys
import django
from django.utils.text import slugify

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from areas.models import ServiceArea

def fix_service_area_slugs():
    print("Fixing ServiceArea slugs...")
    
    # First, temporarily remove the unique constraint for the slug field
    # by creating a custom migration
    
    # Let's see what ServiceAreas exist
    areas = ServiceArea.objects.all()
    
    print(f"Found {areas.count()} service areas:")
    for area in areas:
        print(f"- {area.name}")
        
    # Since we have duplicate default slugs, let's manually fix them
    for i, area in enumerate(areas):
        base_slug = slugify(area.name)
        if not base_slug:
            base_slug = f"area-{i+1}"
        
        # Check if slug already exists
        counter = 1
        new_slug = base_slug
        while ServiceArea.objects.filter(slug=new_slug).exists():
            new_slug = f"{base_slug}-{counter}"
            counter += 1
        
        # Update the slug directly in SQL to avoid unique constraint
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE areas_servicearea SET slug = %s WHERE id = %s",
                [new_slug, area.id]
            )
        
        print(f"Updated {area.name} -> {new_slug}")
    
    print("All slugs updated successfully!")

if __name__ == '__main__':
    fix_service_area_slugs()
