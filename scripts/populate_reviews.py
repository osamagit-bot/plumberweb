#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from areas.models import Review, ServiceArea

def create_reviews():
    """Create sample reviews from different platforms"""
    
    # Get service areas for foreign key relationships
    areas = list(ServiceArea.objects.all())
    
    reviews_data = [
        {
            'customer_name': 'John Smith',
            'platform': 'google',
            'rating': 5,
            'review_text': 'Outstanding plumbing service! They fixed our water heater issue quickly and professionally. The technician was knowledgeable and explained everything clearly. Highly recommend SPRO Plumbing!',
            'review_url': 'https://g.co/kgs/review1',
            'is_featured': True,
            'is_verified': True,
        },
        {
            'customer_name': 'Emily Davis',
            'platform': 'google',
            'rating': 5,
            'review_text': 'Excellent emergency service! Had a major leak at midnight and they were there within 2 hours. Professional, efficient, and reasonably priced. Will definitely use them again.',
            'review_url': 'https://g.co/kgs/review2',
            'is_featured': True,
            'is_verified': True,
        },
        {
            'customer_name': 'Michael Johnson',
            'platform': 'yelp',
            'rating': 4,
            'review_text': 'Good service for drain cleaning. The plumber arrived on time and got the job done. Fair pricing and professional work. Would recommend to others.',
            'review_url': 'https://yelp.com/review1',
            'is_featured': False,
            'is_verified': True,
        },
        {
            'customer_name': 'Rachel Green',
            'platform': 'google',
            'rating': 5,
            'review_text': 'SPRO Plumbing installed our new bathroom fixtures and did an amazing job. Clean work, attention to detail, and completed on schedule. Very satisfied with the results!',
            'review_url': 'https://g.co/kgs/review3',
            'is_featured': True,
            'is_verified': True,
        },
        {
            'customer_name': 'Tom Wilson',
            'platform': 'trustpilot',
            'rating': 5,
            'review_text': 'Fantastic service from start to finish. They diagnosed our plumbing issue quickly and provided a fair quote. The repair was done professionally and hasn\'t had any problems since.',
            'review_url': 'https://trustpilot.com/review1',
            'is_featured': True,
            'is_verified': True,
        },
        {
            'customer_name': 'Susan Lee',
            'platform': 'google',
            'rating': 4,
            'review_text': 'Reliable plumbing service. Fixed our toilet and faucet issues efficiently. The technician was courteous and cleaned up after the work. Good value for money.',
            'review_url': 'https://g.co/kgs/review4',
            'is_featured': False,
            'is_verified': True,
        },
        {
            'customer_name': 'Alex Rodriguez',
            'platform': 'yelp',
            'rating': 5,
            'review_text': 'Best plumbing company in Toronto! They\'ve helped us multiple times with different issues. Always professional, punctual, and reasonably priced. Highly recommend!',
            'review_url': 'https://yelp.com/review2',
            'is_featured': True,
            'is_verified': True,
        },
        {
            'customer_name': 'Jennifer Taylor',
            'platform': 'google',
            'rating': 5,
            'review_text': 'Excellent work on our kitchen plumbing renovation. They handled everything from pipe installation to fixture setup. Professional team and great communication throughout.',
            'review_url': 'https://g.co/kgs/review5',
            'is_featured': True,
            'is_verified': True,
        },
        {
            'customer_name': 'Mark Anderson',
            'platform': 'reddit',
            'rating': 4,
            'review_text': 'Used SPRO Plumbing for sewer line cleaning. They used camera inspection to identify the problem and cleared the blockage effectively. Good service and fair pricing.',
            'review_url': 'https://reddit.com/review1',
            'is_featured': False,
            'is_verified': False,
        },
        {
            'customer_name': 'Lisa Chen',
            'platform': 'google',
            'rating': 5,
            'review_text': 'Outstanding customer service! They explained all options clearly and completed the water heater replacement efficiently. Clean work and professional attitude throughout.',
            'review_url': 'https://g.co/kgs/review6',
            'is_featured': True,
            'is_verified': True,
        },
        {
            'customer_name': 'David Park',
            'platform': 'trustpilot',
            'rating': 4,
            'review_text': 'Solid plumbing service. They fixed our shower pressure issue and installed new fixtures. Work was done professionally and on time. Would use again.',
            'review_url': 'https://trustpilot.com/review2',
            'is_featured': False,
            'is_verified': True,
        },
        {
            'customer_name': 'Karen White',
            'platform': 'google',
            'rating': 5,
            'review_text': 'Exceptional emergency plumbing service! They responded immediately to our burst pipe emergency and prevented major water damage. True professionals!',
            'review_url': 'https://g.co/kgs/review7',
            'is_featured': True,
            'is_verified': True,
        },
    ]
    
    created_count = 0
    
    for i, review_data in enumerate(reviews_data):
        # Assign service area if available
        if areas:
            review_data['service_area'] = areas[i % len(areas)]
        
        review, created = Review.objects.get_or_create(
            customer_name=review_data['customer_name'],
            review_text=review_data['review_text'],
            defaults=review_data
        )
        
        if created:
            created_count += 1
            print(f"✓ Created review: {review.customer_name} - {review.rating} stars ({review.get_platform_display()})")
        else:
            print(f"- Review already exists: {review.customer_name}")
    
    print(f"\nSummary: {created_count} new reviews created out of {len(reviews_data)} total reviews.")

if __name__ == '__main__':
    print("Creating reviews...")
    create_reviews()
    print("Done!")