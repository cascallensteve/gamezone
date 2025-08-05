from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, UserProfile, EquipmentCategory, Equipment, EquipmentImage,
    Rental, Payment, Review, Message, Wishlist
)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'role', 'is_email_verified', 'is_active', 'date_joined']
    list_filter = ['role', 'is_email_verified', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('role', 'phone_number', 'is_email_verified', 'email_verification_token')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {
            'fields': ('email', 'role', 'phone_number')
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'state', 'is_verified', 'total_rentals_as_renter', 'total_rentals_as_owner', 'created_at']
    list_filter = ['is_verified', 'gaming_experience', 'country', 'created_at']
    search_fields = ['user__username', 'user__email', 'city', 'state']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']

class EquipmentImageInline(admin.TabularInline):
    model = EquipmentImage
    extra = 1

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'category', 'condition', 'daily_rate', 'status', 'created_at']
    list_filter = ['category', 'condition', 'status', 'is_available_for_pickup', 'is_available_for_delivery']
    search_fields = ['title', 'brand', 'model', 'owner__username']
    readonly_fields = ['id', 'created_at', 'updated_at', 'total_rentals', 'total_revenue']
    inlines = [EquipmentImageInline]

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'renter', 'owner', 'start_date', 'end_date', 'status', 'total_amount']
    list_filter = ['status', 'delivery_required', 'start_date', 'created_at']
    search_fields = ['equipment__title', 'renter__username', 'owner__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'start_date'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['rental', 'payer', 'payment_type', 'amount', 'status', 'created_at']
    list_filter = ['payment_type', 'status', 'created_at']
    search_fields = ['rental__equipment__title', 'payer__username']
    readonly_fields = ['id', 'created_at']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'reviewee', 'equipment', 'reviewer_type', 'rating', 'created_at']
    list_filter = ['reviewer_type', 'rating', 'is_public', 'created_at']
    search_fields = ['reviewer__username', 'reviewee__username', 'equipment__title']
    readonly_fields = ['id', 'created_at', 'updated_at']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'subject', 'is_read', 'is_system_message', 'created_at']
    list_filter = ['is_read', 'is_system_message', 'created_at']
    search_fields = ['sender__username', 'recipient__username', 'subject']
    readonly_fields = ['id', 'created_at']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'equipment', 'notify_when_available', 'max_daily_rate', 'created_at']
    list_filter = ['notify_when_available', 'created_at']
    search_fields = ['user__username', 'equipment__title']
