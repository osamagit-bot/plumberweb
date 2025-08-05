import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from blog.models import BlogPost
from services.models import Service
from areas.models import ServiceArea

def populate_blog():
    print("Populating blog posts...")
    
    blog_posts = [
        {
            'title': '5 Signs You Need Emergency Drain Cleaning',
            'category': 'maintenance',
            'excerpt': 'Learn the warning signs that indicate you need immediate professional drain cleaning services.',
            'content': '''
Water backing up in your sink, shower, or bathtub is never a good sign. Here are five critical warning signs that indicate you need emergency drain cleaning services:

## 1. Multiple Drains Are Backing Up
When more than one drain in your home is backing up simultaneously, this usually indicates a problem with your main sewer line. This is a serious issue that requires immediate professional attention.

## 2. Sewage Odors
If you smell sewage coming from your drains, this could indicate a blockage in your sewer line or a problem with your septic system. These odors are not only unpleasant but can also be hazardous to your health.

## 3. Gurgling Sounds
Strange gurgling sounds coming from your drains, especially when you flush the toilet or run water elsewhere in the house, indicate air trapped in your plumbing system due to a blockage.

## 4. Water Backing Up
If water is backing up into your sinks, tubs, or floor drains, you have a serious blockage that needs immediate attention. This can cause water damage and create unsanitary conditions.

## 5. Slow Draining Throughout the House
While one slow drain might just need a simple cleaning, multiple slow drains throughout your house indicate a more serious problem with your main sewer line.

If you're experiencing any of these signs, don't wait. Contact SPRO Plumbing immediately for emergency drain cleaning services. Our experienced technicians are available 24/7 to resolve your drainage issues quickly and effectively.
            ''',
            'tags': 'drain cleaning, emergency plumbing, sewer line, maintenance',
            'related_service': 'Emergency Drain Cleaning'
        },
        {
            'title': 'How to Maintain Your Water Heater for Longevity',
            'category': 'maintenance',
            'excerpt': 'Simple maintenance tips to extend your water heater\'s lifespan and improve efficiency.',
            'content': '''
Your water heater is one of the hardest-working appliances in your home. With proper maintenance, you can extend its lifespan and ensure it operates efficiently for years to come.

## Annual Maintenance Tasks

### 1. Flush the Tank
Sediment buildup is the enemy of water heater efficiency. Flush your tank annually to remove mineral deposits that can cause corrosion and reduce heating efficiency.

### 2. Check the Anode Rod
The anode rod protects your tank from corrosion. Check it every 2-3 years and replace it when it's heavily corroded.

### 3. Test the Pressure Relief Valve
This safety device prevents dangerous pressure buildup. Test it annually by lifting the lever briefly to ensure it's working properly.

## Monthly Checks

- Check for leaks around the base and connections
- Listen for unusual noises during operation
- Monitor water temperature consistency

## Signs You Need Professional Service

- Rusty or discolored water
- Strange noises (popping, crackling)
- Inconsistent water temperature
- Higher energy bills
- Age over 8-10 years

Regular maintenance can prevent costly repairs and extend your water heater's life by several years. Contact SPRO Plumbing for professional water heater maintenance and inspection services.
            ''',
            'tags': 'water heater, maintenance, energy efficiency, home care',
            'related_service': 'Water Heater Installation'
        },
        {
            'title': 'Winter Plumbing Preparation: Protect Your Pipes',
            'category': 'seasonal',
            'excerpt': 'Essential steps to winterize your plumbing and prevent costly freeze damage.',
            'content': '''
Winter weather can wreak havoc on your plumbing system. Frozen pipes can burst, causing thousands of dollars in water damage. Here's how to protect your home:

## Before the Freeze

### Insulate Exposed Pipes
Wrap pipes in unheated areas like basements, crawl spaces, and garages with pipe insulation or heat tape.

### Seal Air Leaks
Caulk cracks and holes near pipes to prevent cold air from reaching them.

### Disconnect Garden Hoses
Remove and store garden hoses. Shut off and drain outdoor water valves.

## During Cold Snaps

### Keep Faucets Dripping
A small trickle of water can prevent pipes from freezing.

### Open Cabinet Doors
Allow warm air to circulate around pipes under sinks.

### Maintain Consistent Temperature
Keep your thermostat at the same temperature day and night.

## If Pipes Freeze

1. Turn off the main water supply
2. Open faucets to relieve pressure
3. Apply gentle heat with a hair dryer
4. Never use open flame or high heat
5. Call a professional if you can't locate the freeze

## Emergency Preparedness

Know where your main water shut-off valve is located and how to operate it. Keep our emergency number handy: (647) 551-8342.

Don't let winter catch you unprepared. Contact SPRO Plumbing for professional winterization services and pipe insulation.
            ''',
            'tags': 'winter plumbing, pipe insulation, freeze protection, seasonal maintenance',
            'related_service': 'Pipe Installation'
        },
        {
            'title': 'DIY vs Professional: When to Call a Plumber',
            'category': 'diy',
            'excerpt': 'Know when you can handle plumbing issues yourself and when to call the professionals.',
            'content': '''
While some plumbing tasks are perfect for DIY enthusiasts, others require professional expertise. Here's how to decide:

## Safe DIY Tasks

### Minor Clogs
- Sink and tub clogs (with plunger or snake)
- Toilet clogs (with plunger)
- Hair removal from drains

### Simple Replacements
- Toilet flappers and chains
- Faucet aerators
- Showerheads
- Toilet seats

### Basic Maintenance
- Cleaning drain stoppers
- Checking for leaks
- Insulating pipes

## Call a Professional For

### Major Installations
- Water heater replacement
- New fixture installation
- Pipe rerouting or replacement

### Complex Repairs
- Sewer line issues
- Gas line work
- Major leaks
- No hot water issues

### Emergency Situations
- Burst pipes
- Sewage backups
- No water pressure
- Gas leaks

## Red Flags: Stop and Call a Pro

- You smell gas
- Water is backing up in multiple drains
- You're not sure what you're doing
- The problem keeps recurring
- You need permits for the work

## The Cost of DIY Mistakes

While DIY can save money, mistakes can be costly:
- Water damage from improper connections
- Code violations requiring expensive fixes
- Voided warranties on fixtures
- Safety hazards from gas line work

When in doubt, call SPRO Plumbing. Our experienced technicians can handle any plumbing challenge safely and efficiently.
            ''',
            'tags': 'DIY plumbing, professional plumber, home maintenance, plumbing tips',
            'related_service': 'Faucet Repair'
        },
        {
            'title': 'The Complete Guide to Toilet Troubleshooting',
            'category': 'diy',
            'excerpt': 'Common toilet problems and step-by-step solutions for homeowners.',
            'content': '''
Toilet problems are among the most common plumbing issues homeowners face. Here's your complete troubleshooting guide:

## Common Problems and Solutions

### Toilet Won't Flush
**Possible Causes:**
- Broken handle or chain
- Warped flapper
- Low water level

**Solutions:**
1. Check the handle connection
2. Adjust or replace the chain
3. Replace a warped flapper
4. Adjust water level in tank

### Toilet Keeps Running
**Possible Causes:**
- Flapper not sealing properly
- Chain too long or short
- Float adjustment needed

**Solutions:**
1. Clean around the flapper seat
2. Adjust chain length
3. Bend float arm or adjust float

### Weak Flush
**Possible Causes:**
- Clogged rim holes
- Low water level
- Partial blockage

**Solutions:**
1. Clean rim holes with wire
2. Adjust water level
3. Use plunger for blockages

### Water on Floor
**Possible Causes:**
- Loose bolts at base
- Worn wax ring
- Cracked tank or bowl

**Solutions:**
1. Tighten bolts (don't over-tighten)
2. Replace wax ring (professional job)
3. Replace toilet if cracked

## When to Call a Professional

- Toilet rocks or moves
- Persistent leaks at base
- Cracks in porcelain
- Multiple recurring problems
- Sewer odors

## Maintenance Tips

- Clean regularly with non-abrasive cleaners
- Don't use toilet as trash can
- Replace parts every 5-7 years
- Check for leaks monthly

For complex toilet issues or installations, trust SPRO Plumbing's experienced technicians.
            ''',
            'tags': 'toilet repair, troubleshooting, DIY, bathroom plumbing',
            'related_service': 'Toilet Installation'
        }
    ]
    
    for post_data in blog_posts:
        try:
            # Get related service if specified
            related_service = None
            if post_data.get('related_service'):
                related_service = Service.objects.filter(name=post_data['related_service']).first()
            
            blog_post, created = BlogPost.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'category': post_data['category'],
                    'excerpt': post_data['excerpt'],
                    'content': post_data['content'],
                    'tags': post_data['tags'],
                    'related_service': related_service,
                    'is_published': True,
                    'is_featured': True if post_data['title'] in ['5 Signs You Need Emergency Drain Cleaning', 'Winter Plumbing Preparation: Protect Your Pipes'] else False
                }
            )
            
            if created:
                print(f"Created blog post: {post_data['title']}")
            else:
                print(f"Blog post already exists: {post_data['title']}")
                
        except Exception as e:
            print(f"Error creating blog post '{post_data['title']}': {e}")
    
    print("Blog posts populated successfully!")

if __name__ == '__main__':
    populate_blog()