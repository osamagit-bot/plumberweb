#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

def run_script(script_name, description):
    """Run a population script and handle any errors"""
    print(f"\n{'='*50}")
    print(f"Running {description}")
    print(f"{'='*50}")
    
    try:
        if script_name == 'locations':
            from scripts.populate_locations import create_locations
            create_locations()
        elif script_name == 'services':
            from scripts.populate_services import create_services
            create_services()
        elif script_name == 'faqs':
            from scripts.populate_faqs import create_faqs
            create_faqs()
        elif script_name == 'testimonials':
            from scripts.populate_testimonials import create_testimonials
            create_testimonials()
        elif script_name == 'reviews':
            from scripts.populate_reviews import create_reviews
            create_reviews()
        elif script_name == 'quotes':
            from scripts.populate_quotes import populate_quotes
            populate_quotes()
        elif script_name == 'blog':
            from scripts.populate_blog import populate_blog
            populate_blog()
        
        print(f"✓ {description} completed successfully!")
        
    except Exception as e:
        print(f"✗ Error running {description}: {str(e)}")
        return False
    
    return True

def main():
    """Run all population scripts in order"""
    print("SPRO Plumbing - Database Population Script")
    print("This script will populate your database with sample data.")
    print("\nNote: Existing records will not be duplicated.")
    
    # Confirm before proceeding
    response = input("\nDo you want to continue? (y/N): ").lower().strip()
    if response not in ['y', 'yes']:
        print("Operation cancelled.")
        return
    
    scripts_to_run = [
        ('locations', 'Service Area Locations Population'),
        ('services', 'Services Population'),
        ('faqs', 'FAQs Population'),
        ('testimonials', 'Testimonials Population'),
        ('reviews', 'Reviews Population'),
        ('quotes', 'Quote Calculators Population'),
        ('blog', 'Blog Posts Population'),
    ]
    
    successful = 0
    total = len(scripts_to_run)
    
    for script_name, description in scripts_to_run:
        if run_script(script_name, description):
            successful += 1
    
    print(f"\n{'='*50}")
    print(f"POPULATION COMPLETE")
    print(f"{'='*50}")
    print(f"Successfully completed: {successful}/{total} scripts")
    
    if successful == total:
        print("🎉 All data has been populated successfully!")
        print("\nYou can now:")
        print("- Check your Django admin panel to see the new data")
        print("- Run 'py manage.py runserver' to start your development server")
        print("- Visit your website to see the populated content")
    else:
        print("⚠️  Some scripts encountered errors. Check the output above for details.")

if __name__ == '__main__':
    main()