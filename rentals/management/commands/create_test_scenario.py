from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rentals.models import (
    UserProfile, EquipmentCategory, Equipment, EquipmentImage, 
    Rental, Review, Message
)
from decimal import Decimal
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Create a test scenario with rental requests and activities'

    def handle(self, *args, **options):
        self.stdout.write('Creating test scenario for equipment owner dashboard...')
        
        # Get or create a test owner
        owner, created = User.objects.get_or_create(
            username='test_owner',
            defaults={
                'email': 'owner@example.com',
                'first_name': 'Test',
                'last_name': 'Owner'
            }
        )
        
        if created:
            owner.set_password('password123')
            owner.save()
            
            # Create owner profile
            UserProfile.objects.get_or_create(
                user=owner,
                defaults={
                    'bio': 'Gaming equipment owner with high-end gear for rent.',
                    'city': 'New York',
                    'state': 'New York',
                    'gaming_experience': 'professional',
                    'is_verified': True,
                    'total_rentals_as_owner': 25,
                    'average_rating_as_owner': Decimal('4.8')
                }
            )
        
        # Get or create test renters
        renters = []
        for i in range(3):
            renter, created = User.objects.get_or_create(
                username=f'test_renter_{i+1}',
                defaults={
                    'email': f'renter{i+1}@example.com',
                    'first_name': f'Renter',
                    'last_name': f'{i+1}'
                }
            )
            
            if created:
                renter.set_password('password123')
                renter.save()
                
                UserProfile.objects.get_or_create(
                    user=renter,
                    defaults={
                        'bio': f'Gaming enthusiast #{i+1}',
                        'city': random.choice(['Brooklyn', 'Manhattan', 'Queens']),
                        'state': 'New York',
                        'gaming_experience': random.choice(['intermediate', 'advanced']),
                        'is_verified': True,
                        'average_rating_as_renter': Decimal(str(round(random.uniform(4.2, 5.0), 1)))
                    }
                )
            
            renters.append(renter)
        
        # Create test equipment for the owner
        categories = EquipmentCategory.objects.all()
        
        test_equipment = [
            {
                'title': 'RTX 4090 Ultimate Gaming Rig',
                'description': 'Top-tier gaming PC with RTX 4090, perfect for 4K gaming and streaming.',
                'brand': 'Custom Build',
                'model': 'Ultimate-4090',
                'category': categories.filter(name='Gaming PCs').first(),
                'daily_rate': Decimal('99.99'),
                'security_deposit': Decimal('600.00'),
            },
            {
                'title': 'PlayStation 5 Pro Setup',
                'description': 'Latest PS5 with premium games and accessories.',
                'brand': 'Sony',
                'model': 'PlayStation 5',
                'category': categories.filter(name='Consoles').first(),
                'daily_rate': Decimal('35.99'),
                'security_deposit': Decimal('250.00'),
            },
            {
                'title': 'Meta Quest 3 VR Bundle',
                'description': 'Complete VR setup with top games and accessories.',
                'brand': 'Meta',
                'model': 'Quest 3',
                'category': categories.filter(name='VR Headsets').first(),
                'daily_rate': Decimal('45.99'),
                'security_deposit': Decimal('300.00'),
            }
        ]
        
        created_equipment = []
        for eq_data in test_equipment:
            equipment, created = Equipment.objects.get_or_create(
                owner=owner,
                title=eq_data['title'],
                defaults={
                    'category': eq_data['category'],
                    'description': eq_data['description'],
                    'brand': eq_data['brand'],
                    'model': eq_data['model'],
                    'condition': 'excellent',
                    'daily_rate': eq_data['daily_rate'],
                    'security_deposit': eq_data['security_deposit'],
                    'status': 'active',
                    'location_city': owner.userprofile.city,
                    'location_state': owner.userprofile.state,
                    'is_available_for_pickup': True,
                    'is_available_for_delivery': True,
                    'delivery_radius_km': 25,
                    'delivery_fee': Decimal('15.00'),
                    'year_purchased': 2023,
                    'average_rating': Decimal('4.9'),
                    'view_count': random.randint(50, 200),
                    'total_rentals': random.randint(5, 15)
                }
            )
            created_equipment.append(equipment)
        
        # Create pending rental requests
        self.stdout.write('Creating pending rental requests...')
        
        for equipment in created_equipment[:2]:  # Create requests for first 2 equipment
            renter = random.choice(renters)
            start_date = date.today() + timedelta(days=random.randint(2, 10))
            end_date = start_date + timedelta(days=random.randint(3, 7))
            
            total_days = (end_date - start_date).days
            subtotal = equipment.daily_rate * total_days
            service_fee = subtotal * Decimal('0.05')
            total_amount = subtotal + service_fee
            
            rental, created = Rental.objects.get_or_create(
                equipment=equipment,
                renter=renter,
                defaults={
                    'owner': owner,
                    'start_date': start_date,
                    'end_date': end_date,
                    'daily_rate': equipment.daily_rate,
                    'total_days': total_days,
                    'subtotal': subtotal,
                    'security_deposit': equipment.security_deposit,
                    'service_fee': service_fee,
                    'total_amount': total_amount,
                    'status': 'pending',
                    'delivery_required': random.choice([True, False]),
                    'renter_notes': f"Excited to try out the {equipment.title}! I have experience with similar equipment."
                }
            )
            
            if created:
                self.stdout.write(f'  - Created pending request from {renter.username} for {equipment.title}')
        
        # Create some active rentals
        self.stdout.write('Creating active rentals...')
        
        if len(created_equipment) > 2:
            for equipment in created_equipment[2:]:  # Use remaining equipment
                renter = random.choice(renters)
                start_date = date.today() - timedelta(days=random.randint(1, 5))
                end_date = start_date + timedelta(days=random.randint(5, 10))
                
                total_days = (end_date - start_date).days
                subtotal = equipment.daily_rate * total_days
                service_fee = subtotal * Decimal('0.05')
                total_amount = subtotal + service_fee
                
                rental, created = Rental.objects.get_or_create(
                    equipment=equipment,
                    renter=renter,
                    defaults={
                        'owner': owner,
                        'start_date': start_date,
                        'end_date': end_date,
                        'daily_rate': equipment.daily_rate,
                        'total_days': total_days,
                        'subtotal': subtotal,
                        'security_deposit': equipment.security_deposit,
                        'service_fee': service_fee,
                        'total_amount': total_amount,
                        'status': 'active',
                        'delivery_required': False,
                        'renter_notes': f"Currently enjoying the {equipment.title}!"
                    }
                )
                
                if created:
                    # Update equipment status
                    equipment.status = 'rented'
                    equipment.save()
                    self.stdout.write(f'  - Created active rental from {renter.username} for {equipment.title}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nTest scenario created successfully!\n'
                f'Owner: {owner.username} (password: password123)\n'
                f'Equipment created: {len(created_equipment)}\n'
                f'Pending requests: {Rental.objects.filter(owner=owner, status="pending").count()}\n'
                f'Active rentals: {Rental.objects.filter(owner=owner, status="active").count()}\n'
                f'\nYou can now log in as test_owner to see the comprehensive dashboard!'
            )
        )
