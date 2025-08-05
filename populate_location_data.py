import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from areas.models import ServiceArea, Review, TrustBadge

# Create service areas
areas_data = [
    {
        'name': 'Hamilton',
        'slug': 'hamilton',
        'phone': '(905) 123-4567',
        'email': 'hamilton@plumberondemand.ca',
        'address': '123 Main Street West, Hamilton, ON L8P 1H6',
        'map_embed': '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d93326.26!2d-79.8711!3d43.2557!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x882c986c27de778f%3A0x28f85b2c71a54f5!2sHamilton%2C%20ON!5e0!3m2!1sen!2sca!4v1234567890" width="100%" height="400" style="border:0;" allowfullscreen="" loading="lazy"></iframe>',
    },
    {
        'name': 'Brampton',
        'slug': 'brampton',
        'phone': '(905) 234-5678',
        'email': 'brampton@plumberondemand.ca',
        'address': '456 Queen Street East, Brampton, ON L6V 1C4',
        'map_embed': '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d92326.26!2d-79.7624!3d43.7315!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x882b15efc896d6a3%3A0x5037b28c7231d90!2sBrampton%2C%20ON!5e0!3m2!1sen!2sca!4v1234567890" width="100%" height="400" style="border:0;" allowfullscreen="" loading="lazy"></iframe>',
    },
    {
        'name': 'Toronto',
        'slug': 'toronto',
        'phone': '(416) 345-6789',
        'email': 'toronto@plumberondemand.ca',
        'address': '789 King Street West, Toronto, ON M5V 1N1',
        'map_embed': '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d184551.90!2d-79.3832!3d43.6532!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89d4cb90d7c63ba5%3A0x323555502ab4c477!2sToronto%2C%20ON!5e0!3m2!1sen!2sca!4v1234567890" width="100%" height="400" style="border:0;" allowfullscreen="" loading="lazy"></iframe>',
    }
]

for area_data in areas_data:
    # Remove slug from area_data since we removed the field
    slug = area_data.pop('slug', None)
    area, created = ServiceArea.objects.get_or_create(
        name=area_data['name'],
        defaults=area_data
    )
    if created:
        print(f"Created service area: {area.name}")

# Create trust badges
badges_data = [
    {'name': 'Licensed & Insured', 'icon': 'certificate', 'description': 'Fully licensed and insured professionals'},
    {'name': 'BBB Accredited', 'icon': 'award', 'description': 'Better Business Bureau accredited business'},
    {'name': '24/7 Emergency', 'icon': 'clock', 'description': 'Round-the-clock emergency service'},
    {'name': 'Satisfaction Guaranteed', 'icon': 'thumbs-up', 'description': '100% satisfaction guarantee on all work'},
]

for badge_data in badges_data:
    badge, created = TrustBadge.objects.get_or_create(
        name=badge_data['name'],
        defaults=badge_data
    )
    if created:
        print(f"Created trust badge: {badge.name}")

# Create reviews for each area
hamilton = ServiceArea.objects.get(name='Hamilton')
brampton = ServiceArea.objects.get(name='Brampton')
toronto = ServiceArea.objects.get(name='Toronto')

reviews_data = [
    # Hamilton reviews
    {
        'customer_name': 'John Smith',
        'platform': 'google',
        'rating': 5,
        'review_text': 'Excellent service in Hamilton! Fixed our burst pipe quickly and professionally. Highly recommend.',
        'service_area': hamilton,
        'is_featured': True
    },
    {
        'customer_name': 'Mary Johnson',
        'platform': 'yelp',
        'rating': 5,
        'review_text': 'Best plumber in Hamilton! Fast response and fair pricing. Will definitely use again.',
        'service_area': hamilton,
        'is_featured': True
    },
    {
        'customer_name': 'David Wilson',
        'platform': 'trustpilot',
        'rating': 4,
        'review_text': 'Great work on our Hamilton home renovation. Professional and clean.',
        'service_area': hamilton,
        'is_featured': True
    },
    # Brampton reviews
    {
        'customer_name': 'Sarah Brown',
        'platform': 'google',
        'rating': 5,
        'review_text': 'Amazing service in Brampton! They arrived within an hour for our emergency.',
        'service_area': brampton,
        'is_featured': True
    },
    {
        'customer_name': 'Mike Davis',
        'platform': 'reddit',
        'rating': 5,
        'review_text': 'Found them on Reddit. Best decision ever! Great Brampton plumbers.',
        'service_area': brampton,
        'is_featured': True
    },
    {
        'customer_name': 'Lisa Chen',
        'platform': 'yelp',
        'rating': 4,
        'review_text': 'Professional service in Brampton. Fixed our water heater perfectly.',
        'service_area': brampton,
        'is_featured': True
    },
    # Toronto reviews
    {
        'customer_name': 'Robert Taylor',
        'platform': 'google',
        'rating': 5,
        'review_text': 'Outstanding Toronto plumbing service! Professional and reliable.',
        'service_area': toronto,
        'is_featured': True
    },
    {
        'customer_name': 'Jennifer Lee',
        'platform': 'trustpilot',
        'rating': 5,
        'review_text': 'Excellent work in downtown Toronto. Highly recommended!',
        'service_area': toronto,
        'is_featured': True
    },
    {
        'customer_name': 'Alex Rodriguez',
        'platform': 'yelp',
        'rating': 4,
        'review_text': 'Great Toronto plumbers. Fixed our drain issue quickly.',
        'service_area': toronto,
        'is_featured': True
    }
]

for review_data in reviews_data:
    review, created = Review.objects.get_or_create(
        customer_name=review_data['customer_name'],
        service_area=review_data['service_area'],
        defaults=review_data
    )
    if created:
        print(f"Created review: {review.customer_name} for {review.service_area.name}")

print("Location data population completed!")