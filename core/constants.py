# Shared constants for the plumber website

# Rating choices used across multiple models
RATING_CHOICES = [(i, i) for i in range(1, 6)]

# Urgency levels for bookings
URGENCY_CHOICES = [
    ('low', 'Low - Within a week'),
    ('medium', 'Medium - Within 2-3 days'),
    ('high', 'High - Within 24 hours'),
    ('emergency', 'Emergency - ASAP'),
]

# Review platforms
PLATFORM_CHOICES = [
    ('google', 'Google'),
    ('yelp', 'Yelp'),
    ('trustpilot', 'Trustpilot'),
    ('reddit', 'Reddit'),
]

# Common Font Awesome icons for services
SERVICE_ICONS = [
    ('wrench', 'Wrench'),
    ('shower', 'Shower'),
    ('tint', 'Water Drop'),
    ('fire', 'Fire/Heat'),
    ('snowflake', 'Cold/AC'),
    ('tools', 'Tools'),
    ('home', 'Home'),
    ('exclamation-triangle', 'Emergency'),
    ('cog', 'Mechanical'),
    ('plug', 'Electrical'),
]
