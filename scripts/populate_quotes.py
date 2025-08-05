import os
import sys
import django
from decimal import Decimal

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from services.models import Service
from quotes.models import QuoteCalculator, QuoteOption

def populate_quotes():
    print("Populating quote calculators...")
    
    # Get services
    services = Service.objects.all()
    
    quote_data = [
        {
            'service_name': 'Emergency Drain Cleaning',
            'base_price': 150.00,
            'labor_rate': 85.00,
            'estimated_hours': 2.0,
            'options': [
                {'name': 'Camera Inspection', 'description': 'Video inspection of drain line', 'price': 125.00},
                {'name': 'Hydro Jetting', 'description': 'High-pressure water cleaning', 'price': 200.00},
                {'name': 'Root Removal', 'description': 'Remove tree roots from pipes', 'price': 175.00},
            ]
        },
        {
            'service_name': 'Water Heater Installation',
            'base_price': 800.00,
            'labor_rate': 95.00,
            'estimated_hours': 4.0,
            'options': [
                {'name': 'Tankless Unit', 'description': 'Upgrade to tankless water heater', 'price': 500.00},
                {'name': 'Expansion Tank', 'description': 'Install thermal expansion tank', 'price': 150.00},
                {'name': 'Gas Line Extension', 'description': 'Extend gas line if needed', 'price': 300.00},
            ]
        },
        {
            'service_name': 'Toilet Installation',
            'base_price': 200.00,
            'labor_rate': 75.00,
            'estimated_hours': 2.5,
            'options': [
                {'name': 'Premium Toilet', 'description': 'Upgrade to high-efficiency toilet', 'price': 250.00},
                {'name': 'Bidet Seat', 'description': 'Add electronic bidet seat', 'price': 400.00},
                {'name': 'Shut-off Valve', 'description': 'Replace old shut-off valve', 'price': 75.00},
            ]
        },
        {
            'service_name': 'Pipe Installation',
            'base_price': 300.00,
            'labor_rate': 90.00,
            'estimated_hours': 3.0,
            'options': [
                {'name': 'Copper Pipes', 'description': 'Use copper instead of PEX', 'price': 200.00},
                {'name': 'Insulation', 'description': 'Insulate new pipes', 'price': 100.00},
                {'name': 'Wall Repair', 'description': 'Drywall repair after installation', 'price': 150.00},
            ]
        },
        {
            'service_name': 'Faucet Repair',
            'base_price': 120.00,
            'labor_rate': 70.00,
            'estimated_hours': 1.5,
            'options': [
                {'name': 'New Faucet', 'description': 'Replace with new faucet', 'price': 180.00},
                {'name': 'Shut-off Valves', 'description': 'Replace under-sink valves', 'price': 85.00},
                {'name': 'Supply Lines', 'description': 'Replace supply lines', 'price': 45.00},
            ]
        },
    ]
    
    for data in quote_data:
        try:
            service = services.filter(name=data['service_name']).first()
            if service:
                calculator, created = QuoteCalculator.objects.get_or_create(
                    service=service,
                    defaults={
                        'base_price': Decimal(str(data['base_price'])),
                        'labor_rate_per_hour': Decimal(str(data['labor_rate'])),
                        'estimated_hours': Decimal(str(data['estimated_hours'])),
                        'is_active': True
                    }
                )
                
                if created:
                    print(f"Created calculator for {service.name}")
                    
                    # Add options
                    for i, option_data in enumerate(data['options']):
                        QuoteOption.objects.create(
                            calculator=calculator,
                            name=option_data['name'],
                            description=option_data['description'],
                            price_modifier=Decimal(str(option_data['price'])),
                            order=i
                        )
                        print(f"  Added option: {option_data['name']}")
                else:
                    print(f"Calculator for {service.name} already exists")
        except Exception as e:
            print(f"Error creating calculator for {data['service_name']}: {e}")
    
    print("Quote calculators populated successfully!")

if __name__ == '__main__':
    populate_quotes()