from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rentals.models import EquipmentCategory, Equipment, UserProfile
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Populate database with sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create equipment categories
        categories_data = [
            {'name': 'Gaming PCs', 'description': 'High-performance gaming computers', 'icon': 'fas fa-desktop'},
            {'name': 'Gaming Laptops', 'description': 'Portable gaming machines', 'icon': 'fas fa-laptop'},
            {'name': 'PlayStation Consoles', 'description': 'Sony PlayStation gaming consoles', 'icon': 'fab fa-playstation'},
            {'name': 'Xbox Consoles', 'description': 'Microsoft Xbox gaming consoles', 'icon': 'fab fa-xbox'},
            {'name': 'Nintendo Consoles', 'description': 'Nintendo gaming systems', 'icon': 'fas fa-gamepad'},
            {'name': 'VR Headsets', 'description': 'Virtual reality gaming equipment', 'icon': 'fas fa-vr-cardboard'},
            {'name': 'Gaming Monitors', 'description': 'High-refresh gaming displays', 'icon': 'fas fa-tv'},
            {'name': 'Gaming Chairs', 'description': 'Ergonomic gaming seating', 'icon': 'fas fa-chair'},
            {'name': 'Gaming Accessories', 'description': 'Controllers, keyboards, mice', 'icon': 'fas fa-mouse'},
        ]
        
        for cat_data in categories_data:
            category, created = EquipmentCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create sample users if they don't exist
        sample_users = [
            {'username': 'gamer_alex', 'email': 'alex@gamezone.com', 'first_name': 'Alex', 'last_name': 'Rodriguez'},
            {'username': 'pro_sarah', 'email': 'sarah@gamezone.com', 'first_name': 'Sarah', 'last_name': 'Chen'},
            {'username': 'tech_marcus', 'email': 'marcus@gamezone.com', 'first_name': 'Marcus', 'last_name': 'Thompson'},
            {'username': 'gamer_jenny', 'email': 'jenny@gamezone.com', 'first_name': 'Jenny', 'last_name': 'Wilson'},
            {'username': 'esports_mike', 'email': 'mike@gamezone.com', 'first_name': 'Mike', 'last_name': 'Davis'},
        ]
        
        for user_data in sample_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'is_active': True
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {user.username}')
                
                # Update user profile
                profile = user.userprofile
                profile.city = random.choice(['Los Angeles', 'New York', 'Chicago', 'Austin', 'Seattle'])
                profile.state = random.choice(['CA', 'NY', 'IL', 'TX', 'WA'])
                profile.gaming_experience = random.choice(['intermediate', 'advanced', 'professional'])
                profile.is_verified = True
                profile.save()
        
        # Create sample equipment
        equipment_data = [
            {
                'title': 'High-End Gaming PC (RTX 4080)',
                'description': 'Powerful gaming rig with latest NVIDIA RTX 4080, perfect for 4K gaming and VR.',
                'brand': 'Custom Built',
                'model': 'RTX 4080 Build',
                'category': 'Gaming PCs',
                'condition': 'excellent',
                'daily_rate': Decimal('35.00'),
                'security_deposit': Decimal('500.00'),
                'specifications': {
                    'GPU': 'NVIDIA RTX 4080',
                    'CPU': 'Intel i7-13700K',
                    'RAM': '32GB DDR5',
                    'Storage': '2TB NVMe SSD'
                }
            },
            {
                'title': 'PlayStation 5 Console',
                'description': 'Latest Sony PS5 with DualSense controller and popular games included.',
                'brand': 'Sony',
                'model': 'PlayStation 5',
                'category': 'PlayStation Consoles',
                'condition': 'very_good',
                'daily_rate': Decimal('20.00'),
                'security_deposit': Decimal('300.00'),
                'specifications': {
                    'Storage': '825GB SSD',
                    'Includes': 'Controller, HDMI cable, power cord'
                }
            },
            {
                'title': 'Meta Quest 3 VR Headset',
                'description': 'Latest VR headset with mixed reality capabilities and extensive game library.',
                'brand': 'Meta',
                'model': 'Quest 3',
                'category': 'VR Headsets',
                'condition': 'excellent',
                'daily_rate': Decimal('25.00'),
                'security_deposit': Decimal('200.00'),
                'specifications': {
                    'Resolution': '2064x2208 per eye',
                    'Storage': '512GB',
                    'Includes': 'Controllers, charging cable, head strap'
                }
            },
            {
                'title': 'Gaming Laptop - ASUS ROG Strix',
                'description': 'Portable gaming powerhouse with RTX 4060 and high refresh display.',
                'brand': 'ASUS',
                'model': 'ROG Strix G16',
                'category': 'Gaming Laptops',
                'condition': 'good',
                'daily_rate': Decimal('30.00'),
                'security_deposit': Decimal('800.00'),
                'specifications': {
                    'GPU': 'NVIDIA RTX 4060',
                    'CPU': 'Intel i7-13650HX',
                    'RAM': '16GB DDR5',
                    'Display': '16" 165Hz QHD'
                }
            },
            {
                'title': 'Xbox Series X Console',
                'description': 'Microsoft\'s flagship console with 4K gaming and Game Pass access.',
                'brand': 'Microsoft',
                'model': 'Xbox Series X',
                'category': 'Xbox Consoles',
                'condition': 'very_good',
                'daily_rate': Decimal('18.00'),
                'security_deposit': Decimal('250.00'),
                'specifications': {
                    'Storage': '1TB NVMe SSD',
                    'Performance': '4K up to 120fps',
                    'Includes': 'Wireless controller, HDMI cable'
                }
            }
        ]
        
        users = list(User.objects.all())
        
        for eq_data in equipment_data:
            category = EquipmentCategory.objects.get(name=eq_data['category'])
            owner = random.choice(users)
            
            equipment, created = Equipment.objects.get_or_create(
                title=eq_data['title'],
                defaults={
                    'owner': owner,
                    'category': category,
                    'description': eq_data['description'],
                    'brand': eq_data['brand'],
                    'model': eq_data['model'],
                    'condition': eq_data['condition'],
                    'daily_rate': eq_data['daily_rate'],
                    'security_deposit': eq_data['security_deposit'],
                    'specifications': eq_data['specifications'],
                    'location_city': owner.userprofile.city,
                    'location_state': owner.userprofile.state,
                    'status': 'active',
                    'is_available_for_pickup': True,
                    'is_available_for_delivery': random.choice([True, False]),
                    'delivery_radius_km': random.randint(0, 50),
                    'average_rating': Decimal(str(round(random.uniform(4.0, 5.0), 1))),
                    'total_rentals': random.randint(0, 25),
                    'view_count': random.randint(50, 500)
                }
            )
            if created:
                self.stdout.write(f'Created equipment: {equipment.title}')
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data!'))
