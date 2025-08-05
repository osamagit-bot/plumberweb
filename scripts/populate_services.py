#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from services.models import Service

def create_services():
    """Create services based on available images"""
    
    services_data = [
        {
            'name': 'Burst Pipe Repair',
            'description': 'Emergency burst pipe repair and replacement services. We respond quickly to minimize water damage and restore your plumbing system.',
            'price_range': '$150 - $500',
            'icon': 'exclamation-triangle',
            'is_emergency': True,
        },
        {
            'name': 'Camera Inspection',
            'description': 'Professional drain and sewer line camera inspection to identify blockages, damage, and potential issues before they become major problems.',
            'price_range': '$200 - $400',
            'icon': 'cog',
            'is_emergency': False,
        },
        {
            'name': 'Drain Cleaning',
            'description': 'Professional drain cleaning services for kitchen sinks, bathroom drains, and main sewer lines. Fast and effective solutions.',
            'price_range': '$100 - $300',
            'icon': 'tint',
            'is_emergency': False,
        },
        {
            'name': 'Faucet Repair & Installation',
            'description': 'Complete faucet repair and installation services for kitchen and bathroom fixtures. Quality workmanship guaranteed.',
            'price_range': '$80 - $250',
            'icon': 'wrench',
            'is_emergency': False,
        },
        {
            'name': 'Garbage Disposal Services',
            'description': 'Garbage disposal installation, repair, and maintenance. Keep your kitchen running smoothly with our expert services.',
            'price_range': '$120 - $350',
            'icon': 'cog',
            'is_emergency': False,
        },
        {
            'name': 'Pipe Installation',
            'description': 'Professional pipe installation and replacement services. We work with all types of piping materials and systems.',
            'price_range': '$200 - $800',
            'icon': 'tools',
            'is_emergency': False,
        },
        {
            'name': 'Sewer Line Cleaning',
            'description': 'Complete sewer line cleaning and maintenance services. Prevent backups and keep your system flowing properly.',
            'price_range': '$250 - $600',
            'icon': 'tint',
            'is_emergency': True,
        },
        {
            'name': 'Shower Repair',
            'description': 'Shower repair and installation services including fixtures, valves, and complete shower systems. Professional results.',
            'price_range': '$150 - $500',
            'icon': 'shower',
            'is_emergency': False,
        },
        {
            'name': 'Toilet Repair & Installation',
            'description': 'Complete toilet repair and installation services. From simple fixes to full replacements, we handle it all.',
            'price_range': '$100 - $400',
            'icon': 'home',
            'is_emergency': False,
        },
        {
            'name': 'Water Heater Services',
            'description': 'Water heater installation, repair, and maintenance for all types including tankless, electric, and gas units.',
            'price_range': '$300 - $1500',
            'icon': 'fire',
            'is_emergency': True,
        },
    ]
    
    created_count = 0
    
    for service_data in services_data:
        service, created = Service.objects.get_or_create(
            name=service_data['name'],
            defaults=service_data
        )
        
        if created:
            created_count += 1
            print(f"✓ Created service: {service.name}")
        else:
            print(f"- Service already exists: {service.name}")
    
    print(f"\nSummary: {created_count} new services created out of {len(services_data)} total services.")

if __name__ == '__main__':
    print("Creating services...")
    create_services()
    print("Done!")