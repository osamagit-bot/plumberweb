import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from areas.models import ServiceArea

# Add more Canadian service areas
new_areas = [
    {
        'name': 'Mississauga',
        'slug': 'mississauga',
        'phone': '(905) 456-7890',
        'email': 'mississauga@plumberondemand.ca',
        'address': '321 Dundas Street West, Mississauga, ON L5B 1H2',
        'map_embed': '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d92326.26!2d-79.6441!3d43.5890!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x882b469fe76b05b7%3A0x3146cbed75966db!2sMississauga%2C%20ON!5e0!3m2!1sen!2sca!4v1234567890" width="100%" height="400" style="border:0;" allowfullscreen="" loading="lazy"></iframe>',
    },
    {
        'name': 'Oakville',
        'slug': 'oakville',
        'phone': '(905) 567-8901',
        'email': 'oakville@plumberondemand.ca',
        'address': '654 Lakeshore Road East, Oakville, ON L6J 1A1',
        'map_embed': '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d92326.26!2d-79.6876!3d43.4675!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x882b5c8b8b8b8b8b%3A0x8b8b8b8b8b8b8b8b!2sOakville%2C%20ON!5e0!3m2!1sen!2sca!4v1234567890" width="100%" height="400" style="border:0;" allowfullscreen="" loading="lazy"></iframe>',
    },
    {
        'name': 'Burlington',
        'slug': 'burlington',
        'phone': '(905) 678-9012',
        'email': 'burlington@plumberondemand.ca',
        'address': '987 Brant Street, Burlington, ON L7R 2J6',
        'map_embed': '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d92326.26!2d-79.7909!3d43.3255!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x882c9c9c9c9c9c9c%3A0x9c9c9c9c9c9c9c9c!2sBurlington%2C%20ON!5e0!3m2!1sen!2sca!4v1234567890" width="100%" height="400" style="border:0;" allowfullscreen="" loading="lazy"></iframe>',
    },
    {
        'name': 'Markham',
        'slug': 'markham',
        'phone': '(905) 789-0123',
        'email': 'markham@plumberondemand.ca',
        'address': '147 Main Street North, Markham, ON L3P 1Y2',
        'map_embed': '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d92326.26!2d-79.2624!3d43.8561!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x882d2d2d2d2d2d2d%3A0x2d2d2d2d2d2d2d2d!2sMarkham%2C%20ON!5e0!3m2!1sen!2sca!4v1234567890" width="100%" height="400" style="border:0;" allowfullscreen="" loading="lazy"></iframe>',
    },
    {
        'name': 'Richmond Hill',
        'slug': 'richmond-hill',
        'phone': '(905) 890-1234',
        'email': 'richmondhill@plumberondemand.ca',
        'address': '258 Yonge Street, Richmond Hill, ON L4C 2T8',
        'map_embed': '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d92326.26!2d-79.4403!3d43.8828!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x882d3d3d3d3d3d3d%3A0x3d3d3d3d3d3d3d3d!2sRichmond%20Hill%2C%20ON!5e0!3m2!1sen!2sca!4v1234567890" width="100%" height="400" style="border:0;" allowfullscreen="" loading="lazy"></iframe>',
    },
    {
        'name': 'Vaughan',
        'slug': 'vaughan',
        'phone': '(905) 901-2345',
        'email': 'vaughan@plumberondemand.ca',
        'address': '369 Major Mackenzie Drive, Vaughan, ON L4J 7Y1',
        'map_embed': '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d92326.26!2d-79.4980!3d43.8361!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x882d4d4d4d4d4d4d%3A0x4d4d4d4d4d4d4d4d!2sVaughan%2C%20ON!5e0!3m2!1sen!2sca!4v1234567890" width="100%" height="400" style="border:0;" allowfullscreen="" loading="lazy"></iframe>',
    }
]

for area_data in new_areas:
    area, created = ServiceArea.objects.get_or_create(
        slug=area_data['slug'],
        defaults=area_data
    )
    if created:
        print(f"Created service area: {area.name}")
    else:
        print(f"Service area already exists: {area.name}")

print("New Canadian service areas added!")