import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from services.models import FAQ

# Create FAQs
faqs_data = [
    {
        'question': 'Do you offer 24/7 emergency plumbing services?',
        'answer': 'Yes! We provide 24/7 emergency plumbing services for urgent issues like burst pipes, major leaks, and sewer backups. Call our emergency line anytime.',
        'order': 1
    },
    {
        'question': 'Are you licensed and insured?',
        'answer': 'Absolutely. We are fully licensed plumbers and carry comprehensive liability insurance for your protection and peace of mind.',
        'order': 2
    },
    {
        'question': 'How quickly can you respond to service calls?',
        'answer': 'For emergency calls, we typically arrive within 1-2 hours. For scheduled appointments, we offer same-day or next-day service in most cases.',
        'order': 3
    },
    {
        'question': 'Do you provide free estimates?',
        'answer': 'Yes, we provide free estimates for most plumbing projects. Contact us to schedule an appointment for your free, no-obligation estimate.',
        'order': 4
    },
    {
        'question': 'What payment methods do you accept?',
        'answer': 'We accept cash, checks, and all major credit cards including Visa, MasterCard, and American Express. We also offer financing options for larger projects.',
        'order': 5
    },
    {
        'question': 'Do you guarantee your work?',
        'answer': 'Yes, we stand behind our work with a satisfaction guarantee. All our services come with a warranty, and we will return to fix any issues at no additional cost.',
        'order': 6
    }
]

for faq_data in faqs_data:
    faq, created = FAQ.objects.get_or_create(
        question=faq_data['question'],
        defaults=faq_data
    )
    if created:
        print(f"Created FAQ: {faq.question}")

print("FAQ data population completed!")