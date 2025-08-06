# SPRO Plumbing Website - Agent Instructions

## Project Overview
Django-based plumber website with location-based services, bookings, testimonials, and contact forms.

## Development Commands

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Testing & Quality
```bash
# Run tests
python manage.py test

# Check for issues
python manage.py check --deploy

# Collect static files (for production)
python manage.py collectstatic --no-input
```

## Project Structure
```
plumber_site/
├── main/              # Main views and forms
├── services/          # Services, testimonials, FAQs
├── bookings/          # Booking and contact models
├── areas/             # Service areas and reviews
├── core/              # Shared constants and utilities
├── templates/         # HTML templates
├── static/           # Static files (CSS, JS, images)
└── plumber_site/     # Django project settings
```

## Key Improvements Made

### Security Enhancements
- ✅ Moved SECRET_KEY to environment variables
- ✅ Added security headers (HSTS, XSS protection, etc.)
- ✅ Implemented Django ModelForms with proper validation
- ✅ Added CSRF protection and secure cookies
- ✅ Updated password hashers to use Argon2

### Database Optimizations
- ✅ Added database indexes on frequently queried fields
- ✅ Improved model relationships with proper on_delete handlers
- ✅ Added model validation with MinValueValidator/MaxValueValidator
- ✅ Implemented proper field choices and constants
- ✅ Added phone number validation with django-phonenumber-field

### Code Quality
- ✅ Created shared constants in core/constants.py
- ✅ Fixed view naming conflicts (services -> services_view)
- ✅ Added select_related for optimized database queries
- ✅ Implemented proper model Meta classes with ordering
- ✅ Added get_absolute_url methods for SEO

### Form Improvements
- ✅ Replaced raw form handling with Django ModelForms
- ✅ Added comprehensive form validation
- ✅ Implemented proper error handling and user feedback
- ✅ Added Tailwind CSS styling for forms

## Environment Variables
Required environment variables (see .env.example):
- DJANGO_SECRET_KEY
- DEBUG
- ALLOWED_HOSTS
- Security flags (SECURE_SSL_REDIRECT, etc.)

## Security Notes
- Never commit .env file to version control
- Use strong SECRET_KEY in production
- Set DEBUG=False in production
- Configure proper ALLOWED_HOSTS
- Enable SSL redirects in production

## Database Models
- **Service**: Plumbing services with emergency categorization
- **Booking**: Customer booking requests with status tracking
- **ContactMessage**: Customer contact form submissions
- **ServiceArea**: Location-based service areas
- **Testimonial**: Customer testimonials and reviews
- **FAQ**: Frequently asked questions
- **Review**: Platform-specific reviews (Google, Yelp, etc.)
- **TrustBadge**: Professional credibility indicators

## Admin Access
- URL: /admin/
- Username: admin
- Password: admin123
- Uses Jazzmin for enhanced admin interface
- All models are properly registered with admin

## Next Steps for Production
1. Set up PostgreSQL database
2. Configure email backend for notifications
3. Add CAPTCHA protection to forms
4. Implement rate limiting
5. Set up proper logging and monitoring
6. Add unit tests for critical functionality
