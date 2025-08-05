import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from services.models import Service, Testimonial

# Create services
services_data = [
    {
        'name': 'Emergency Drain Cleaning',
        'description': 'Fast and effective drain cleaning for clogged sinks, toilets, and floor drains. Available 24/7 for emergency situations.',
        'price_range': '$150 - $300',
        'icon': 'tint',
        'is_emergency': True
    },
    {
        'name': 'Burst Pipe Repair',
        'description': 'Immediate response for burst pipes to prevent water damage. Professional pipe repair and replacement services.',
        'price_range': '$200 - $500',
        'icon': 'exclamation-triangle',
        'is_emergency': True
    },
    {
        'name': 'Water Heater Emergency',
        'description': 'Emergency water heater repair and replacement. No hot water? We can fix it fast.',
        'price_range': '$300 - $800',
        'icon': 'fire',
        'is_emergency': True
    },
    {
        'name': 'Toilet Installation',
        'description': 'Professional toilet installation and replacement. High-efficiency models available.',
        'price_range': '$200 - $400',
        'icon': 'toilet',
        'is_emergency': False
    },
    {
        'name': 'Faucet Repair & Installation',
        'description': 'Kitchen and bathroom faucet repair, replacement, and installation services.',
        'price_range': '$100 - $250',
        'icon': 'faucet',
        'is_emergency': False
    },
    {
        'name': 'Pipe Installation',
        'description': 'New pipe installation for renovations and new construction. Copper, PVC, and PEX piping.',
        'price_range': '$300 - $1000',
        'icon': 'wrench',
        'is_emergency': False
    },
    {
        'name': 'Sewer Line Cleaning',
        'description': 'Professional sewer line cleaning and inspection using advanced camera technology.',
        'price_range': '$250 - $500',
        'icon': 'search',
        'is_emergency': False
    },
    {
        'name': 'Garbage Disposal Service',
        'description': 'Garbage disposal repair, installation, and maintenance services.',
        'price_range': '$150 - $350',
        'icon': 'cog',
        'is_emergency': False
    }
]

for service_data in services_data:
    service, created = Service.objects.get_or_create(
        name=service_data['name'],
        defaults=service_data
    )
    if created:
        print(f"Created service: {service.name}")

# Create testimonials
testimonials_data = [
    {
        'customer_name': 'Sarah Johnson',
        'rating': 5,
        'comment': 'Excellent service! They fixed my burst pipe quickly and professionally. Highly recommend ProPlumber for any emergency plumbing needs.'
    },
    {
        'customer_name': 'Mike Rodriguez',
        'rating': 5,
        'comment': 'Fast response time and fair pricing. The technician was knowledgeable and explained everything clearly. Will definitely use them again.'
    },
    {
        'customer_name': 'Emily Chen',
        'rating': 4,
        'comment': 'Great work on our bathroom renovation. Professional installation of new fixtures and very clean work area. Thank you!'
    },
    {
        'customer_name': 'David Thompson',
        'rating': 5,
        'comment': 'Called them for an emergency drain cleaning at 2 AM. They arrived within an hour and had everything working perfectly. Amazing service!'
    },
    {
        'customer_name': 'Lisa Williams',
        'rating': 5,
        'comment': 'Professional, reliable, and honest. They diagnosed the problem quickly and provided a fair estimate. Excellent customer service.'
    }
]

for testimonial_data in testimonials_data:
    testimonial, created = Testimonial.objects.get_or_create(
        customer_name=testimonial_data['customer_name'],
        defaults=testimonial_data
    )
    if created:
        print(f"Created testimonial: {testimonial.customer_name}")

print("Data population completed!")