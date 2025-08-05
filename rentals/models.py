from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.conf import settings
from decimal import Decimal
import uuid

class CustomUser(AbstractUser):
    """
    Custom User model with role-based access
    """
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('admin', 'Administrator'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"{self.email} ({self.role})"
    
    def is_customer(self):
        return self.role == 'customer'
    
    def is_vendor(self):
        return self.role == 'vendor'
    
    def is_admin_user(self):
        return self.role == 'admin'

class UserProfile(models.Model):
    """
    Extended user profile for additional gaming-specific information
    Rationale: Core user data for trust, verification, and personalization
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    
    # Trust and verification
    is_verified = models.BooleanField(default=False)
    verification_document = models.ImageField(upload_to='verification/', blank=True, null=True)
    verification_date = models.DateTimeField(blank=True, null=True)
    
    # Gaming preferences
    favorite_genres = models.CharField(max_length=200, blank=True)
    gaming_experience = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('professional', 'Professional')
        ],
        default='intermediate'
    )
    
    # Location
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='USA')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    # Platform metrics
    total_rentals_as_renter = models.PositiveIntegerField(default=0)
    total_rentals_as_owner = models.PositiveIntegerField(default=0)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    average_rating_as_renter = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    average_rating_as_owner = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class EquipmentCategory(models.Model):
    """
    Categories for equipment organization
    Rationale: Structured classification for efficient searching and filtering
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # Font Awesome icon class
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Equipment Categories"
    
    def __str__(self):
        return self.name

class Equipment(models.Model):
    """
    Core equipment model with comprehensive specifications
    Rationale: Detailed equipment data ensures accurate matching and informed decisions
    """
    CONDITION_CHOICES = [
        ('excellent', 'Excellent - Like new'),
        ('very_good', 'Very Good - Minor wear'),
        ('good', 'Good - Normal wear'),
        ('fair', 'Fair - Some wear but fully functional')
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('active', 'Active'),
        ('rented', 'Currently Rented'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended')
    ]
    
    # Basic Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_equipment')
    category = models.ForeignKey(EquipmentCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Specifications
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year_purchased = models.PositiveIntegerField(blank=True, null=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    specifications = models.JSONField(default=dict, blank=True)  # Store flexible specs
    
    # Pricing
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('1.00'))])
    weekly_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    monthly_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    security_deposit = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    
    # Availability
    is_available_for_pickup = models.BooleanField(default=True)
    is_available_for_delivery = models.BooleanField(default=False)
    delivery_radius_km = models.PositiveIntegerField(default=0)  # 0 means no delivery
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    
    # Location (can differ from owner's location)
    location_city = models.CharField(max_length=100)
    location_state = models.CharField(max_length=100)
    location_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    location_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    # Status and Metrics
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    total_rentals = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    view_count = models.PositiveIntegerField(default=0)
    
    # Additional Information
    included_accessories = models.TextField(blank=True)
    usage_instructions = models.TextField(blank=True)
    special_requirements = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_rented = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} by {self.owner.username}"

class EquipmentImage(models.Model):
    """
    Multiple images per equipment
    Rationale: Visual verification crucial for rental decisions
    """
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='equipment/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', 'uploaded_at']
    
    def __str__(self):
        return f"Image for {self.equipment.title}"

class Rental(models.Model):
    """
    Core rental transaction model
    Rationale: Complete rental lifecycle tracking for business operations and analytics
    """
    STATUS_CHOICES = [
        ('pending', 'Pending Owner Approval'),
        ('approved', 'Approved'),
        ('payment_pending', 'Payment Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active Rental'),
        ('returned', 'Returned'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('disputed', 'Disputed')
    ]
    
    # Basic Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    renter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rentals_as_renter')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rentals_as_owner')
    
    # Rental Period
    start_date = models.DateField()
    end_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    
    # Pricing
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2)  # Snapshot at booking time
    total_days = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=8, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    service_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Delivery/Pickup
    delivery_required = models.BooleanField(default=False)
    delivery_address = models.TextField(blank=True)
    pickup_instructions = models.TextField(blank=True)
    
    # Status and Workflow
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_at = models.DateTimeField(blank=True, null=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    # Notes
    renter_notes = models.TextField(blank=True)
    owner_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Rental of {self.equipment.title} by {self.renter.username}"

class Payment(models.Model):
    """
    Payment tracking for rentals
    Rationale: Financial transparency and audit trail for all transactions
    """
    PAYMENT_TYPES = [
        ('rental_payment', 'Rental Payment'),
        ('security_deposit', 'Security Deposit'),
        ('delivery_fee', 'Delivery Fee'),
        ('late_fee', 'Late Fee'),
        ('damage_fee', 'Damage Fee'),
        ('refund', 'Refund')
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('disputed', 'Disputed')
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
        ('manual', 'Manual'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, related_name='payments')
    payer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='paypal')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # PayPal Integration
    paypal_payment_id = models.CharField(max_length=255, blank=True, null=True)
    paypal_order_id = models.CharField(max_length=255, blank=True, null=True)
    paypal_capture_id = models.CharField(max_length=255, blank=True, null=True)
    
    # Payment Gateway Integration (Legacy)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_charge_id = models.CharField(max_length=255, blank=True, null=True)
    
    # Additional PayPal fields
    paypal_payer_id = models.CharField(max_length=255, blank=True, null=True)
    paypal_email = models.EmailField(blank=True, null=True)
    
    processed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.payment_type} - ${self.amount} - {self.status}"

class Review(models.Model):
    """
    Bidirectional review system
    Rationale: Trust building through community feedback
    """
    REVIEWER_TYPES = [
        ('renter_to_owner', 'Renter reviewing Owner'),
        ('owner_to_renter', 'Owner reviewing Renter'),
        ('equipment_review', 'Equipment Review')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given')
    reviewee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_received')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='reviews')
    
    reviewer_type = models.CharField(max_length=20, choices=REVIEWER_TYPES)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField(blank=True)
    
    # Specific rating categories
    communication_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True)
    condition_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True)
    timeliness_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True)
    
    is_public = models.BooleanField(default=True)
    helpful_votes = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['rental', 'reviewer', 'reviewer_type']
    
    def __str__(self):
        return f"{self.reviewer_type} - {self.rating} stars"

class Message(models.Model):
    """
    Communication system between users
    Rationale: Facilitate coordination and resolve disputes
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, related_name='messages', blank=True, null=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    
    is_read = models.BooleanField(default=False)
    is_system_message = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"

class Wishlist(models.Model):
    """
    User wishlist for equipment
    Rationale: Help users track desired equipment and notify of availability
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='wishlisted_by')
    notify_when_available = models.BooleanField(default=True)
    max_daily_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'equipment']
    
    def __str__(self):
        return f"{self.user.username}'s wishlist - {self.equipment.title}"

class Sensor(models.Model):
    """
    Database sensor model for equipment tracking
    Rationale: Track equipment status, location, and usage patterns
    """
    SENSOR_TYPES = [
        ('location', 'Location Tracker'),
        ('usage', 'Usage Monitor'),
        ('condition', 'Condition Monitor'),
        ('temperature', 'Temperature Sensor'),
        ('humidity', 'Humidity Sensor'),
        ('motion', 'Motion Sensor'),
        ('battery', 'Battery Level'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance'),
        ('error', 'Error'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    sensor_type = models.CharField(max_length=20, choices=SENSOR_TYPES)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='sensors', blank=True, null=True)
    
    # Sensor data
    current_value = models.CharField(max_length=255, blank=True, null=True)
    last_reading = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Location data (if applicable)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    altitude = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    
    # Configuration
    is_active = models.BooleanField(default=True)
    reading_interval_minutes = models.PositiveIntegerField(default=60)  # How often to read
    alert_threshold = models.CharField(max_length=255, blank=True, null=True)  # JSON field for thresholds
    
    # Metadata
    description = models.TextField(blank=True)
    manufacturer = models.CharField(max_length=100, blank=True)
    model_number = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_sensor_type_display()})"
    
    def get_latest_reading(self):
        """Get the most recent sensor reading"""
        return SensorReading.objects.filter(sensor=self).order_by('-timestamp').first()
    
    def is_online(self):
        """Check if sensor is online (has recent readings)"""
        if not self.last_reading:
            return False
        from django.utils import timezone
        return (timezone.now() - self.last_reading).total_seconds() < 3600  # 1 hour

class SensorReading(models.Model):
    """
    Individual sensor readings
    Rationale: Store historical sensor data for analytics and monitoring
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='readings')
    
    # Reading data
    value = models.CharField(max_length=255)  # Store as string, can be parsed based on sensor type
    unit = models.CharField(max_length=20, blank=True)  # e.g., 'C', 'F', 'm', 'km/h'
    
    # Location (if applicable)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    altitude = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    
    # Metadata
    quality_score = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)  # 0-1
    is_alert = models.BooleanField(default=False)  # If reading triggered an alert
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['sensor', '-timestamp']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.sensor.name} - {self.value} {self.unit} at {self.timestamp}"
