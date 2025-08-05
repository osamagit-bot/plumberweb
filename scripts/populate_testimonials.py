#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from services.models import Testimonial, Service
from areas.models import ServiceArea

def create_testimonials():
    """Create sample testimonials"""
    
    # Get some services and areas for foreign key relationships
    services = list(Service.objects.all())
    areas = list(ServiceArea.objects.all())
    
    testimonials_data = [
        {
            'customer_name': 'Sarah Johnson',
            'email': 'sarah.j@email.com',
            'phone': '+14165551234',
            'title': 'Excellent Emergency Service',
            'rating': 5,
            'comment': 'Had a burst pipe at 2 AM and SPRO Plumbing was there within an hour! Professional, efficient, and saved my basement from major flooding. Highly recommend their emergency services.',
            'is_featured': True,
            'is_verified': True,
            'google_review_url': 'https://g.co/kgs/example1',
        },
        {
            'customer_name': 'Mike Chen',
            'email': 'mike.chen@email.com',
            'phone': '+14165555678',
            'title': 'Great Water Heater Installation',
            'rating': 5,
            'comment': 'Replaced my old water heater with a new tankless unit. The team was knowledgeable, clean, and completed the job on time. Great value for money!',
            'is_featured': True,
            'is_verified': True,
        },
        {
            'customer_name': 'Jennifer Martinez',
            'email': 'j.martinez@email.com',
            'title': 'Professional Drain Cleaning',
            'rating': 4,
            'comment': 'Quick response for drain cleaning service. The technician explained everything clearly and the drains are working perfectly now. Will use again.',
            'is_featured': False,
            'is_verified': True,
        },
        {
            'customer_name': 'David Thompson',
            'phone': '+14165559876',
            'title': 'Reliable Faucet Repair',
            'rating': 5,
            'comment': 'Fixed my kitchen faucet leak quickly and efficiently. Fair pricing and excellent workmanship. The technician was courteous and professional.',
            'is_featured': True,
            'is_verified': False,
        },
        {
            'customer_name': 'Lisa Wong',
            'email': 'lisa.wong@email.com',
            'title': 'Shower Installation Excellence',
            'rating': 5,
            'comment': 'Complete bathroom renovation including new shower installation. The work was done to perfection and on schedule. Couldn\'t be happier with the results!',
            'is_featured': True,
            'is_verified': True,
            'google_review_url': 'https://g.co/kgs/example2',
        },
        {
            'customer_name': 'Robert Kim',
            'phone': '+14165554321',
            'title': 'Toilet Repair Service',
            'rating': 4,
            'comment': 'Prompt service for toilet repair. The plumber arrived on time and fixed the issue quickly. Good communication throughout the process.',
            'is_featured': False,
            'is_verified': True,
        },
        {
            'customer_name': 'Amanda Foster',
            'email': 'amanda.f@email.com',
            'title': 'Sewer Line Cleaning',
            'rating': 5,
            'comment': 'Had recurring sewer backup issues. SPRO Plumbing used camera inspection to identify the problem and cleaned the line thoroughly. No issues since!',
            'is_featured': True,
            'is_verified': True,
        },
        {
            'customer_name': 'James Wilson',
            'phone': '+14165558765',
            'title': 'Pipe Installation Project',
            'rating': 5,
            'comment': 'Major pipe replacement project handled professionally from start to finish. Clean work, fair pricing, and excellent customer service.',
            'is_featured': False,
            'is_verified': True,
        },
        {
            'customer_name': 'Maria Rodriguez',
            'email': 'maria.r@email.com',
            'title': 'Garbage Disposal Installation',
            'rating': 4,
            'comment': 'Installed new garbage disposal unit. The technician was knowledgeable and explained proper maintenance. Good service overall.',
            'is_featured': False,
            'is_verified': False,
        },
        {
            'customer_name': 'Kevin Brown',
            'phone': '+14165552468',
            'title': 'Emergency Plumbing Service',
            'rating': 5,
            'comment': 'Called for emergency plumbing service on a Sunday. They responded quickly and resolved the issue efficiently. Great emergency response team!',
            'is_featured': True,
            'is_verified': True,
            'google_review_url': 'https://g.co/kgs/example3',
        },
    ]
    
    created_count = 0
    
    for i, testimonial_data in enumerate(testimonials_data):
        # Assign service and area if available
        if services:
            testimonial_data['service'] = services[i % len(services)]
        if areas:
            testimonial_data['location'] = areas[i % len(areas)]
        
        testimonial, created = Testimonial.objects.get_or_create(
            customer_name=testimonial_data['customer_name'],
            comment=testimonial_data['comment'],
            defaults=testimonial_data
        )
        
        if created:
            created_count += 1
            print(f"✓ Created testimonial: {testimonial.customer_name} - {testimonial.rating} stars")
        else:
            print(f"- Testimonial already exists: {testimonial.customer_name}")
    
    print(f"\nSummary: {created_count} new testimonials created out of {len(testimonials_data)} total testimonials.")

if __name__ == '__main__':
    print("Creating testimonials...")
    create_testimonials()
    print("Done!")