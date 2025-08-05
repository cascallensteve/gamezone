from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rentals.models import (
    UserProfile, EquipmentCategory, Equipment, EquipmentImage, 
    Rental, Review, Message, Wishlist
)
from decimal import Decimal
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Populate database with sample gaming equipment rental data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data for GameZone...')
        
        # Create sample users
        self.create_sample_users()
        
        # Create equipment categories
        self.create_equipment_categories()
        
        # Create sample equipment
        self.create_sample_equipment()
        
        # Create sample rentals
        self.create_sample_rentals()
        
        # Create sample reviews
        self.create_sample_reviews()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )

    def create_sample_users(self):
        """Create sample users with profiles"""
        self.stdout.write('Creating sample users...')
        
        users_data = [
            {
                'username': 'gamer_alex',
                'email': 'alex@example.com',
                'first_name': 'Alex',
                'last_name': 'Johnson',
                'bio': 'Hardcore gamer with a passion for FPS and RPGs. Own multiple high-end gaming setups.',
                'city': 'San Francisco',
                'state': 'California',
                'gaming_experience': 'professional'
            },
            {
                'username': 'casual_sarah',
                'email': 'sarah@example.com', 
                'first_name': 'Sarah',
                'last_name': 'Chen',
                'bio': 'Casual gamer who loves indie games and co-op adventures.',
                'city': 'Austin',
                'state': 'Texas',
                'gaming_experience': 'intermediate'
            },
            {
                'username': 'tech_mike',
                'email': 'mike@example.com',
                'first_name': 'Mike',
                'last_name': 'Rodriguez',
                'bio': 'Tech enthusiast and VR pioneer. Always testing the latest gaming hardware.',
                'city': 'Seattle',
                'state': 'Washington',
                'gaming_experience': 'advanced'
            },
            {
                'username': 'streamer_emma',
                'email': 'emma@example.com',
                'first_name': 'Emma',
                'last_name': 'Wilson',
                'bio': 'Content creator and Twitch streamer. Need high-quality equipment for streams.',
                'city': 'Los Angeles',
                'state': 'California',
                'gaming_experience': 'professional'
            }
        ]
        
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name']
                }
            )
            
            if created:
                user.set_password('password123')
                user.save()
                
                # Create user profile
                UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'bio': user_data['bio'],
                        'city': user_data['city'],
                        'state': user_data['state'],
                        'gaming_experience': user_data['gaming_experience'],
                        'is_verified': True,
                        'total_rentals_as_renter': random.randint(0, 15),
                        'total_rentals_as_owner': random.randint(0, 10),
                        'average_rating_as_renter': Decimal(str(round(random.uniform(4.0, 5.0), 1))),
                        'average_rating_as_owner': Decimal(str(round(random.uniform(4.0, 5.0), 1)))
                    }
                )

    def create_equipment_categories(self):
        """Create equipment categories"""
        self.stdout.write('Creating equipment categories...')
        
        categories = [
            {'name': 'Gaming PCs', 'description': 'High-performance gaming desktops', 'icon': 'fas fa-desktop'},
            {'name': 'Gaming Laptops', 'description': 'Portable gaming machines', 'icon': 'fas fa-laptop'},
            {'name': 'Consoles', 'description': 'PlayStation, Xbox, Nintendo Switch', 'icon': 'fas fa-gamepad'},
            {'name': 'VR Headsets', 'description': 'Virtual reality equipment', 'icon': 'fas fa-vr-cardboard'},
            {'name': 'Monitors', 'description': 'Gaming monitors and displays', 'icon': 'fas fa-tv'},
            {'name': 'Audio', 'description': 'Gaming headsets and speakers', 'icon': 'fas fa-headphones'},
            {'name': 'Accessories', 'description': 'Controllers, keyboards, mice', 'icon': 'fas fa-mouse'},
            {'name': 'Streaming Gear', 'description': 'Cameras, microphones, capture cards', 'icon': 'fas fa-broadcast-tower'}
        ]
        
        for cat_data in categories:
            EquipmentCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'icon': cat_data['icon']
                }
            )

    def create_sample_equipment(self):
        """Create sample gaming equipment"""
        self.stdout.write('Creating sample equipment...')
        
        users = User.objects.all()
        categories = EquipmentCategory.objects.all()
        
        equipment_data = [
            # Gaming PCs
            {
                'title': 'RTX 4090 Gaming Beast',
                'description': 'Ultimate gaming PC with RTX 4090, i9-13900K, 32GB DDR5 RAM. Perfect for 4K gaming and streaming.',
                'brand': 'Custom Build',
                'model': 'RTX4090-Beast',
                'category': 'Gaming PCs',
                'condition': 'excellent',
                'daily_rate': Decimal('89.99'),
                'security_deposit': Decimal('500.00'),
                'specifications': {
                    'GPU': 'NVIDIA RTX 4090',
                    'CPU': 'Intel i9-13900K',
                    'RAM': '32GB DDR5',
                    'Storage': '2TB NVMe SSD',
                    'PSU': '1000W Gold'
                }
            },
            {
                'title': 'AMD Ryzen 7 Gaming Rig',
                'description': 'High-performance AMD build with RX 7800 XT. Great for 1440p gaming.',
                'brand': 'Custom Build',
                'model': 'AMD-Powerhouse',
                'category': 'Gaming PCs',
                'condition': 'very_good',
                'daily_rate': Decimal('65.99'),
                'security_deposit': Decimal('400.00'),
                'specifications': {
                    'GPU': 'AMD RX 7800 XT',
                    'CPU': 'AMD Ryzen 7 7700X',
                    'RAM': '16GB DDR5',
                    'Storage': '1TB NVMe SSD',
                    'PSU': '750W Gold'
                }
            },
            # Gaming Laptops
            {
                'title': 'ASUS ROG Strix G15',
                'description': 'Portable gaming laptop with RTX 3070, perfect for gaming on the go.',
                'brand': 'ASUS',
                'model': 'ROG Strix G15',
                'category': 'Gaming Laptops',
                'condition': 'excellent',
                'daily_rate': Decimal('45.99'),
                'security_deposit': Decimal('300.00'),
                'specifications': {
                    'GPU': 'NVIDIA RTX 3070',
                    'CPU': 'AMD Ryzen 7 5800H',
                    'RAM': '16GB DDR4',
                    'Storage': '512GB SSD',
                    'Display': '15.6" 144Hz'
                }
            },
            # Consoles
            {
                'title': 'PlayStation 5 Console',
                'description': 'Latest PS5 console with DualSense controller and popular games included.',
                'brand': 'Sony',
                'model': 'PlayStation 5',
                'category': 'Consoles',
                'condition': 'excellent',
                'daily_rate': Decimal('29.99'),
                'security_deposit': Decimal('200.00'),
                'specifications': {
                    'Storage': '825GB SSD',
                    'CPU': 'AMD Zen 2',
                    'GPU': 'AMD RDNA 2',
                    'Controllers': '1x DualSense',
                    'Extras': 'Spider-Man Miles Morales, Horizon Forbidden West'
                }
            },
            {
                'title': 'Xbox Series X',
                'description': 'Microsoft\'s flagship console with Game Pass Ultimate included.',
                'brand': 'Microsoft',
                'model': 'Xbox Series X',
                'category': 'Consoles',
                'condition': 'very_good',
                'daily_rate': Decimal('27.99'),
                'security_deposit': Decimal('200.00'),
                'specifications': {
                    'Storage': '1TB SSD',
                    'CPU': 'AMD Zen 2',
                    'GPU': 'AMD RDNA 2',
                    'Controllers': '1x Wireless Controller',
                    'Extras': 'Game Pass Ultimate (3 months)'
                }
            },
            # VR Headsets
            {
                'title': 'Meta Quest 3 VR Headset',
                'description': 'Latest VR headset with mixed reality capabilities. Includes top VR games.',
                'brand': 'Meta',
                'model': 'Quest 3',
                'category': 'VR Headsets',
                'condition': 'excellent',
                'daily_rate': Decimal('39.99'),
                'security_deposit': Decimal('250.00'),
                'specifications': {
                    'Resolution': '2064x2208 per eye',
                    'Storage': '128GB',
                    'Tracking': '6DOF inside-out',
                    'Controllers': '2x Touch Plus',
                    'Extras': 'Beat Saber, Half-Life Alyx'
                }
            },
            # Monitors
            {
                'title': 'ASUS ROG Swift 32" 4K',
                'description': '32" 4K gaming monitor with 144Hz refresh rate and G-Sync.',
                'brand': 'ASUS',
                'model': 'ROG Swift PG32UQX',
                'category': 'Monitors',
                'condition': 'excellent',
                'daily_rate': Decimal('35.99'),
                'security_deposit': Decimal('200.00'),
                'specifications': {
                    'Size': '32 inches',
                    'Resolution': '3840x2160 (4K)',
                    'Refresh Rate': '144Hz',
                    'Panel': 'IPS',
                    'Features': 'G-Sync Compatible, HDR'
                }
            },
            # Audio
            {
                'title': 'SteelSeries Arctis Pro Wireless',
                'description': 'Premium wireless gaming headset with Hi-Res audio.',
                'brand': 'SteelSeries',
                'model': 'Arctis Pro Wireless',
                'category': 'Audio',
                'condition': 'very_good',
                'daily_rate': Decimal('15.99'),
                'security_deposit': Decimal('50.00'),
                'specifications': {
                    'Type': 'Wireless Gaming Headset',
                    'Battery': '20+ hours',
                    'Audio': 'Hi-Res certified',
                    'Microphone': 'Retractable',
                    'Compatibility': 'PC, PS5, Xbox, Switch'
                }
            },
            # Streaming Gear
            {
                'title': 'Elgato Stream Deck + Camera Setup',
                'description': 'Complete streaming setup with Stream Deck, webcam, and lighting.',
                'brand': 'Elgato',
                'model': 'Streaming Pro Kit',
                'category': 'Streaming Gear',
                'condition': 'excellent',
                'daily_rate': Decimal('25.99'),
                'security_deposit': Decimal('150.00'),
                'specifications': {
                    'Stream Deck': '15 LCD keys',
                    'Camera': '1080p 60fps webcam',
                    'Lighting': 'Key Light',
                    'Microphone': 'USB condenser mic',
                    'Software': 'OBS Studio configured'
                }
            }
        ]
        
        for eq_data in equipment_data:
            category = EquipmentCategory.objects.get(name=eq_data['category'])
            owner = random.choice(users)
            
            equipment = Equipment.objects.create(
                owner=owner,
                category=category,
                title=eq_data['title'],
                description=eq_data['description'],
                brand=eq_data['brand'],
                model=eq_data['model'],
                condition=eq_data['condition'],
                daily_rate=eq_data['daily_rate'],
                security_deposit=eq_data['security_deposit'],
                specifications=eq_data['specifications'],
                status='active',
                location_city=owner.userprofile.city,
                location_state=owner.userprofile.state,
                is_available_for_pickup=True,
                is_available_for_delivery=random.choice([True, False]),
                delivery_radius_km=random.randint(0, 50),
                delivery_fee=Decimal(str(random.randint(0, 25))),
                year_purchased=random.randint(2020, 2024),
                total_rentals=random.randint(0, 25),
                average_rating=Decimal(str(round(random.uniform(4.0, 5.0), 1))),
                view_count=random.randint(10, 500)
            )

    def create_sample_rentals(self):
        """Create sample rental transactions"""
        self.stdout.write('Creating sample rentals...')
        
        equipment_list = list(Equipment.objects.all())
        users = list(User.objects.all())
        
        for _ in range(15):
            equipment = random.choice(equipment_list)
            renter = random.choice([u for u in users if u != equipment.owner])
            
            start_date = date.today() + timedelta(days=random.randint(-30, 30))
            end_date = start_date + timedelta(days=random.randint(1, 7))
            
            total_days = (end_date - start_date).days
            subtotal = equipment.daily_rate * total_days
            service_fee = subtotal * Decimal('0.05')
            total_amount = subtotal + service_fee
            
            status_choices = ['pending', 'approved', 'confirmed', 'active', 'completed', 'cancelled']
            status = random.choice(status_choices)
            
            Rental.objects.create(
                equipment=equipment,
                renter=renter,
                owner=equipment.owner,
                start_date=start_date,
                end_date=end_date,
                daily_rate=equipment.daily_rate,
                total_days=total_days,
                subtotal=subtotal,
                security_deposit=equipment.security_deposit,
                service_fee=service_fee,
                total_amount=total_amount,
                status=status,
                delivery_required=random.choice([True, False]),
                renter_notes=f"Looking forward to using the {equipment.title}!"
            )

    def create_sample_reviews(self):
        """Create sample reviews"""
        self.stdout.write('Creating sample reviews...')
        
        completed_rentals = Rental.objects.filter(status='completed')
        
        review_comments = [
            "Great equipment, exactly as described!",
            "Smooth transaction and excellent gaming experience.",
            "Equipment was in perfect condition, highly recommend!",
            "Fast communication and easy pickup process.",
            "Amazing setup, will definitely rent again!",
            "Professional owner and top-quality gear.",
            "Exceeded expectations, 5 stars!",
            "Perfect for my gaming weekend.",
            "Clean, well-maintained equipment.",
            "Great value for the rental price."
        ]
        
        for rental in completed_rentals:
            # Renter reviewing equipment/owner
            if random.choice([True, False]):
                Review.objects.create(
                    rental=rental,
                    reviewer=rental.renter,
                    reviewee=rental.owner,
                    equipment=rental.equipment,
                    reviewer_type='renter_to_owner',
                    rating=random.randint(4, 5),
                    title=f"Great experience with {rental.equipment.title}",
                    comment=random.choice(review_comments),
                    communication_rating=random.randint(4, 5),
                    condition_rating=random.randint(4, 5),
                    timeliness_rating=random.randint(4, 5)
                )
            
            # Owner reviewing renter
            if random.choice([True, False]):
                Review.objects.create(
                    rental=rental,
                    reviewer=rental.owner,
                    reviewee=rental.renter,
                    equipment=rental.equipment,
                    reviewer_type='owner_to_renter',
                    rating=random.randint(4, 5),
                    title=f"Reliable renter",
                    comment="Responsible renter, returned equipment in perfect condition.",
                    communication_rating=random.randint(4, 5),
                    timeliness_rating=random.randint(4, 5)
                )
