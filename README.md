# ProPlumber - Dynamic Plumber Website

A fully dynamic plumber website built with Django backend and Tailwind CSS frontend, featuring a professional blue and white color scheme.

## Features

### Frontend Features
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Professional UI**: Clean blue/white color palette
- **Interactive Elements**: Dynamic forms, mobile menu, hover effects
- **Service Showcase**: Detailed service pages with emergency/regular categorization
- **Customer Testimonials**: Dynamic testimonial display
- **Online Booking**: Comprehensive booking form with urgency levels
- **Contact System**: Contact form with business information
- **Location-Based Pages**: Dynamic content for multiple service areas
- **Review Integration**: Multi-platform review display (Google, Yelp, Trustpilot, Reddit)
- **Trust Badges**: Professional credibility indicators

### Backend Features
- **Django Admin**: Full admin interface for managing content
- **Dynamic Content**: Services, testimonials, bookings, and messages
- **Database Models**: Structured data for services, bookings, testimonials, and contacts
- **Form Handling**: Secure form processing with CSRF protection
- **Message System**: Success/error message display
- **Multi-Location Support**: Service area management with location-specific content
- **Review Management**: Platform-specific review system
- **CRM Integration Ready**: Booking and contact form backend

## Installation & Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Populate Sample Data**:
   ```bash
   python populate_data.py
   python populate_location_data.py
   ```

4. **Create Superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

5. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```

## Admin Access

- **URL**: http://localhost:8000/admin/
- **Username**: admin
- **Password**: admin123

## Project Structure

```
plumber_site/
├── main/              # Main app (views, URLs)
├── services/          # Services and testimonials models
├── bookings/          # Booking and contact models
├── areas/             # Location management
├── blog/              # Blog functionality
├── quotes/            # Quote calculator
├── monitoring/        # Health checks & monitoring
├── core/              # Shared utilities
├── templates/         # HTML templates
├── static/            # Static files (CSS, JS, images)
├── media/             # User uploaded files
├── scripts/           # Management & backup scripts
├── docs/              # Documentation
├── deployment/        # Production configs
├── logs/              # Application logs
├── backups/           # Backup storage
└── plumber_site/      # Django project settings
```

## Pages

### Main Pages
1. **Home** (`/`) - Hero section, features, services preview, testimonials
2. **Services** (`/services/`) - Complete service listings with emergency/regular categories
3. **Booking** (`/booking/`) - Online appointment booking form
4. **Contact** (`/contact/`) - Contact form and business information

### Location-Specific Pages
1. **Hamilton** (`/hamilton/`) - hamilton.plumberondemand.ca equivalent
2. **Brampton** (`/brampton/`) - brampton.plumberondemand.ca equivalent
3. **Toronto** (`/toronto/`) - Dynamic location-based content

Each location has its own:
- Home page with local content
- Services page (`/{location}/services/`)
- Booking page (`/{location}/booking/`)
- Contact page (`/{location}/contact/`)
- Local phone numbers and addresses
- Location-specific reviews and testimonials

## Customization

### Colors
The website uses a blue/white color scheme defined in Tailwind config:
- Primary Blue: `#1e40af`
- Light Blue: `#3b82f6`
- Dark Blue: `#1e3a8a`

### Adding Services
Use Django admin to add/edit services:
1. Go to `/admin/`
2. Navigate to Services section
3. Add new services with icons, descriptions, and pricing

### Managing Bookings
All booking requests appear in Django admin under Bookings section.

## Technologies Used

- **Backend**: Django 4.2.7
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Database**: SQLite (development)
- **Icons**: Font Awesome 6.0
- **Styling**: Tailwind CSS via CDN

## Features Included

✅ Responsive design
✅ Service management
✅ Online booking system
✅ Contact forms
✅ Customer testimonials
✅ Emergency service highlighting
✅ Admin interface
✅ Professional styling
✅ Mobile navigation
✅ Form validation
✅ Success/error messages
✅ **Dynamic location-based content**
✅ **Multi-platform review integration**
✅ **Trust badges and credibility indicators**
✅ **Location-specific phone numbers and addresses**
✅ **Google Maps integration ready**
✅ **CRM/scheduling tool integration ready**
✅ **Subdomain-ready architecture**

## Next Steps

- Add Google Maps integration
- Implement payment processing
- Add email notifications
- Create customer portal
- Add photo galleries
- Implement SEO optimization
- Add live chat functionality