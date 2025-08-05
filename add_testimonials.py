import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from services.models import Testimonial, Service

# Add 3 more testimonials
new_testimonials = [
    {
        'customer_name': 'Jennifer Wilson',
        'rating': 5,
        'comment': 'Outstanding emergency service! They fixed our burst pipe at 2 AM. Professional, fast, and reasonably priced. Highly recommend!',
    },
    {
        'customer_name': 'Michael Chen',
        'rating': 4,
        'comment': 'Great experience with their drain cleaning service. Technician was knowledgeable and explained everything clearly. Will use again.',
    },
    {
        'customer_name': 'Sarah Thompson',
        'rating': 5,
        'comment': 'Excellent water heater installation. Clean work, on time, and fair pricing. The team was courteous and professional throughout.',
    }
]

for testimonial_data in new_testimonials:
    testimonial, created = Testimonial.objects.get_or_create(
        customer_name=testimonial_data['customer_name'],
        defaults=testimonial_data
    )
    if created:
        print(f"Created testimonial: {testimonial.customer_name}")
    else:
        print(f"Testimonial already exists: {testimonial.customer_name}")

print("3 more testimonials added!")