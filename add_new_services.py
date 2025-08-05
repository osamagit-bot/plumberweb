#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from services.models import Service

def add_new_services():
    """Add Camera Inspection and Shower Repair services"""
    
    new_services = [
        {
            'name': 'Camera Inspection',
            'description': 'Professional video pipe inspection to diagnose plumbing issues. Our advanced camera technology helps identify blockages, leaks, and pipe damage without invasive digging.',
            'price_range': '$200 - $400',
            'is_emergency': False,
        },
        {
            'name': 'Shower Repair',
            'description': 'Complete shower repair services including fixing leaks, replacing fixtures, repairing tiles, and resolving water pressure issues. Get your shower working perfectly again.',
            'price_range': '$150 - $600',
            'is_emergency': False,
        }
    ]
    
    created_count = 0
    
    for service_data in new_services:
        # Check if service already exists
        if Service.objects.filter(name=service_data['name']).exists():
            print(f"Service '{service_data['name']}' already exists, skipping...")
            continue
        
        # Create the service
        service = Service.objects.create(**service_data)
        created_count += 1
        print(f"Created: {service.name} - {service.price_range}")
    
    print(f"\nSummary:")
    print(f"Created {created_count} new services")
    print(f"Total services in database: {Service.objects.count()}")

if __name__ == '__main__':
    add_new_services()
