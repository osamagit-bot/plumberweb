#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from services.models import FAQ

def create_faqs():
    """Create frequently asked questions"""
    
    faqs_data = [
        {
            'question': 'What are your service hours?',
            'answer': 'We offer 24/7 emergency plumbing services. Our regular business hours are Monday to Friday 8 AM to 6 PM, and Saturday 9 AM to 4 PM. Emergency services are available outside these hours.',
            'category': 'General',
            'order': 1,
        },
        {
            'question': 'Do you provide free estimates?',
            'answer': 'Yes, we provide free estimates for most plumbing services. Our technician will assess your plumbing issue and provide you with a detailed quote before any work begins.',
            'category': 'Pricing',
            'order': 2,
        },
        {
            'question': 'Are you licensed and insured?',
            'answer': 'Absolutely! We are fully licensed, bonded, and insured. All our technicians are certified professionals with years of experience in the plumbing industry.',
            'category': 'Credentials',
            'order': 3,
        },
        {
            'question': 'What payment methods do you accept?',
            'answer': 'We accept cash, checks, and all major credit cards including Visa, MasterCard, and American Express. We also offer financing options for larger projects.',
            'category': 'Payment',
            'order': 4,
        },
        {
            'question': 'How quickly can you respond to emergencies?',
            'answer': 'For emergency plumbing situations, we typically respond within 1-2 hours. We understand that plumbing emergencies can cause significant damage, so we prioritize urgent calls.',
            'category': 'Emergency',
            'order': 5,
        },
        {
            'question': 'Do you guarantee your work?',
            'answer': 'Yes, we stand behind our work with a comprehensive warranty. Labor is guaranteed for 1 year, and parts come with manufacturer warranties. Your satisfaction is our priority.',
            'category': 'Warranty',
            'order': 6,
        },
        {
            'question': 'What should I do if I have a burst pipe?',
            'answer': 'First, turn off your main water supply immediately. Then, turn off electricity to the affected area if there is standing water. Call us right away for emergency repair services.',
            'category': 'Emergency',
            'order': 7,
        },
        {
            'question': 'How often should I have my drains cleaned?',
            'answer': 'We recommend professional drain cleaning every 1-2 years for preventive maintenance. However, if you notice slow drains, gurgling sounds, or bad odors, you should have them cleaned sooner.',
            'category': 'Maintenance',
            'order': 8,
        },
        {
            'question': 'Can you work on weekends?',
            'answer': 'Yes, we offer weekend services including Saturdays and emergency services on Sundays. Weekend rates may apply for non-emergency services.',
            'category': 'Scheduling',
            'order': 9,
        },
        {
            'question': 'What areas do you serve?',
            'answer': 'We serve the Greater Toronto Area including Toronto, Mississauga, Brampton, Markham, Richmond Hill, Vaughan, and surrounding communities. Contact us to confirm service in your area.',
            'category': 'Service Area',
            'order': 10,
        },
        {
            'question': 'How do I know if I need to replace my water heater?',
            'answer': 'Signs you may need a new water heater include: age over 8-12 years, rusty water, strange noises, leaks around the base, or inconsistent water temperature. We can assess and recommend the best solution.',
            'category': 'Water Heater',
            'order': 11,
        },
        {
            'question': 'What causes low water pressure?',
            'answer': 'Low water pressure can be caused by clogged pipes, faulty pressure regulators, water leaks, or mineral buildup. Our technicians can diagnose and fix the underlying issue.',
            'category': 'Troubleshooting',
            'order': 12,
        },
    ]
    
    created_count = 0
    
    for faq_data in faqs_data:
        faq, created = FAQ.objects.get_or_create(
            question=faq_data['question'],
            defaults=faq_data
        )
        
        if created:
            created_count += 1
            print(f"✓ Created FAQ: {faq.question}")
        else:
            print(f"- FAQ already exists: {faq.question}")
    
    print(f"\nSummary: {created_count} new FAQs created out of {len(faqs_data)} total FAQs.")

if __name__ == '__main__':
    print("Creating FAQs...")
    create_faqs()
    print("Done!")