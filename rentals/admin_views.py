from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Count, Sum, Q, Avg
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import Equipment, Rental, UserProfile, EquipmentCategory, Sensor, SensorReading, Payment
from .paypal_service import initiate_payment
from datetime import datetime, timedelta
import json

def superuser_required(user):
    return user.is_superuser

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    """Main admin dashboard with overview statistics"""
    
    # Get current date and calculate date ranges
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)
    seven_days_ago = today - timedelta(days=7)
    
    # User statistics
    total_users = User.objects.count()
    new_users_30d = User.objects.filter(date_joined__gte=thirty_days_ago).count()
    active_users = User.objects.filter(last_login__gte=seven_days_ago).count()
    
    # Equipment statistics
    total_equipment = Equipment.objects.count()
    active_equipment = Equipment.objects.filter(status='active').count()
    pending_equipment = Equipment.objects.filter(status='pending').count()
    
    # Rental statistics
    total_rentals = Rental.objects.count()
    active_rentals = Rental.objects.filter(status__in=['confirmed', 'active']).count()
    completed_rentals = Rental.objects.filter(status='completed').count()
    
    # Revenue statistics
    total_revenue = Rental.objects.filter(status='completed').aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    monthly_revenue = Rental.objects.filter(
        status='completed',
        created_at__gte=thirty_days_ago
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Recent activity (last 10 items)
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_equipment = Equipment.objects.select_related('owner').order_by('-created_at')[:5]
    recent_rentals = Rental.objects.select_related('equipment', 'renter').order_by('-created_at')[:5]
    
    # Charts data for dashboard
    # User growth over last 30 days
    user_growth_data = []
    for i in range(30):
        date = today - timedelta(days=29-i)
        count = User.objects.filter(date_joined__date=date).count()
        user_growth_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })
    
    # Equipment by category
    equipment_by_category = list(Equipment.objects.values('category__name').annotate(
        count=Count('id')
    ).order_by('-count')[:5])
    
    context = {
        'total_users': total_users,
        'new_users_30d': new_users_30d,
        'active_users': active_users,
        'total_equipment': total_equipment,
        'active_equipment': active_equipment,
        'pending_equipment': pending_equipment,
        'total_rentals': total_rentals,
        'active_rentals': active_rentals,
        'completed_rentals': completed_rentals,
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenue,
        'recent_users': recent_users,
        'recent_equipment': recent_equipment,
        'recent_rentals': recent_rentals,
        'user_growth_data': json.dumps(user_growth_data),
        'equipment_by_category': json.dumps(equipment_by_category),
    }
    
    return render(request, 'admin/dashboard.html', context)

@user_passes_test(lambda u: u.is_staff)
def admin_users(request):
    """User management page"""
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    user_type = request.GET.get('type', 'all')
    status = request.GET.get('status', 'all')
    
    # Base queryset
    users = User.objects.select_related('userprofile').annotate(
        equipment_count=Count('equipment'),
        rental_count=Count('rental_as_renter')
    )
    
    # Apply filters
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    if user_type == 'staff':
        users = users.filter(is_staff=True)
    elif user_type == 'owners':
        users = users.filter(equipment_count__gt=0)
    elif user_type == 'renters':
        users = users.filter(rental_count__gt=0)
    
    if status == 'active':
        users = users.filter(is_active=True)
    elif status == 'inactive':
        users = users.filter(is_active=False)
    
    # Pagination
    paginator = Paginator(users.order_by('-date_joined'), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'user_type': user_type,
        'status': status,
    }
    
    return render(request, 'admin/users.html', context)

@user_passes_test(lambda u: u.is_staff)
def admin_user_detail(request, user_id):
    """Individual user detail and management"""
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'toggle_active':
            user.is_active = not user.is_active
            user.save()
            status = 'activated' if user.is_active else 'deactivated'
            messages.success(request, f'User {status} successfully.')
            
        elif action == 'toggle_staff':
            user.is_staff = not user.is_staff
            user.save()
            status = 'granted' if user.is_staff else 'revoked'
            messages.success(request, f'Staff privileges {status} successfully.')
            
        return redirect('admin_user_detail', user_id=user.id)
    
    # Get user statistics
    user_equipment = Equipment.objects.filter(owner=user).order_by('-created_at')
    user_rentals_as_renter = Rental.objects.filter(renter=user).select_related('equipment').order_by('-created_at')
    user_rentals_as_owner = Rental.objects.filter(equipment__owner=user).select_related('equipment', 'renter').order_by('-created_at')
    
    total_earned = user_rentals_as_owner.filter(status='completed').aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    total_spent = user_rentals_as_renter.filter(status='completed').aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    context = {
        'user_obj': user,
        'user_equipment': user_equipment[:10],
        'user_rentals_as_renter': user_rentals_as_renter[:10],
        'user_rentals_as_owner': user_rentals_as_owner[:10],
        'total_earned': total_earned,
        'total_spent': total_spent,
    }
    
    return render(request, 'admin/user_detail.html', context)

@user_passes_test(lambda u: u.is_staff)
def admin_equipment(request):
    """Equipment management page"""
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', 'all')
    status_filter = request.GET.get('status', 'all')
    
    # Base queryset
    equipment = Equipment.objects.select_related('owner', 'category').annotate(
        rental_count=Count('rental')
    )
    
    # Apply filters
    if search_query:
        equipment = equipment.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(model__icontains=search_query)
        )
    
    if category_filter != 'all':
        equipment = equipment.filter(category__name=category_filter)
    
    if status_filter != 'all':
        equipment = equipment.filter(status=status_filter)
    
    # Get categories for filter
    categories = EquipmentCategory.objects.filter(is_active=True)
    
    # Pagination
    paginator = Paginator(equipment.order_by('-created_at'), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'status_filter': status_filter,
    }
    
    return render(request, 'admin/equipment.html', context)

@user_passes_test(lambda u: u.is_staff)
def admin_equipment_detail(request, equipment_id):
    """Individual equipment detail and management"""
    equipment = get_object_or_404(Equipment, id=equipment_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            equipment.status = 'active'
            equipment.save()
            messages.success(request, 'Equipment approved successfully.')
            
        elif action == 'reject':
            equipment.status = 'rejected'
            equipment.save()
            messages.success(request, 'Equipment rejected.')
            
        elif action == 'suspend':
            equipment.status = 'suspended'
            equipment.save()
            messages.success(request, 'Equipment suspended.')
            
        return redirect('admin_equipment_detail', equipment_id=equipment.id)
    
    # Get equipment rentals
    equipment_rentals = Rental.objects.filter(equipment=equipment).select_related('renter').order_by('-created_at')
    
    # Calculate statistics
    total_rentals = equipment_rentals.count()
    total_revenue = equipment_rentals.filter(status='completed').aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    context = {
        'equipment': equipment,
        'equipment_rentals': equipment_rentals[:10],
        'total_rentals': total_rentals,
        'total_revenue': total_revenue,
    }
    
    return render(request, 'admin/equipment_detail.html', context)

@user_passes_test(lambda u: u.is_staff)
def admin_rentals(request):
    """Rental management page"""
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', 'all')
    date_filter = request.GET.get('date', 'all')
    
    # Base queryset
    rentals = Rental.objects.select_related('equipment', 'renter', 'equipment__owner')
    
    # Apply filters
    if search_query:
        rentals = rentals.filter(
            Q(equipment__title__icontains=search_query) |
            Q(renter__username__icontains=search_query) |
            Q(equipment__owner__username__icontains=search_query)
        )
    
    if status_filter != 'all':
        rentals = rentals.filter(status=status_filter)
    
    if date_filter == 'today':
        today = timezone.now().date()
        rentals = rentals.filter(created_at__date=today)
    elif date_filter == 'week':
        week_ago = timezone.now().date() - timedelta(days=7)
        rentals = rentals.filter(created_at__date__gte=week_ago)
    elif date_filter == 'month':
        month_ago = timezone.now().date() - timedelta(days=30)
        rentals = rentals.filter(created_at__date__gte=month_ago)
    
    # Pagination
    paginator = Paginator(rentals.order_by('-created_at'), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'date_filter': date_filter,
    }
    
    return render(request, 'admin/rentals.html', context)

@user_passes_test(lambda u: u.is_staff)
def admin_rental_detail(request, rental_id):
    """Individual rental detail and management"""
    rental = get_object_or_404(Rental, id=rental_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'cancel':
            rental.status = 'cancelled'
            rental.save()
            messages.success(request, 'Rental cancelled successfully.')
            
        elif action == 'complete':
            rental.status = 'completed'
            rental.save()
            messages.success(request, 'Rental marked as completed.')
            
        return redirect('admin_rental_detail', rental_id=rental.id)
    
    context = {
        'rental': rental,
    }
    
    return render(request, 'admin/rental_detail.html', context)

@user_passes_test(lambda u: u.is_staff)
def admin_categories(request):
    """Category management page"""
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            name = request.POST.get('name')
            description = request.POST.get('description')
            
            if name:
                EquipmentCategory.objects.create(
                    name=name,
                    description=description,
                    is_active=True
                )
                messages.success(request, 'Category created successfully.')
            else:
                messages.error(request, 'Category name is required.')
        
        elif action == 'toggle':
            category_id = request.POST.get('category_id')
            category = get_object_or_404(EquipmentCategory, id=category_id)
            category.is_active = not category.is_active
            category.save()
            status = 'activated' if category.is_active else 'deactivated'
            messages.success(request, f'Category {status} successfully.')
        
        return redirect('admin_categories')
    
    categories = EquipmentCategory.objects.annotate(
        equipment_count=Count('equipment')
    ).order_by('-is_active', 'name')
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'admin/categories.html', context)

@user_passes_test(lambda u: u.is_staff)
def admin_analytics(request):
    """Analytics and reporting page"""
    
    # Date range calculations
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)
    
    # User analytics
    user_stats = {
        'total_users': User.objects.count(),
        'new_users_this_month': User.objects.filter(date_joined__gte=thirty_days_ago).count(),
        'active_users': User.objects.filter(last_login__gte=thirty_days_ago).count(),
    }
    
    # Equipment analytics
    equipment_stats = {
        'total_equipment': Equipment.objects.count(),
        'active_equipment': Equipment.objects.filter(status='active').count(),
        'pending_approval': Equipment.objects.filter(status='pending').count(),
    }
    
    # Rental analytics
    rental_stats = {
        'total_rentals': Rental.objects.count(),
        'active_rentals': Rental.objects.filter(status__in=['confirmed', 'active']).count(),
        'completed_rentals': Rental.objects.filter(status='completed').count(),
        'total_revenue': Rental.objects.filter(status='completed').aggregate(
            total=Sum('total_amount')
        )['total'] or 0,
    }
    
    # Top categories
    top_categories = list(Equipment.objects.values('category__name').annotate(
        count=Count('id')
    ).order_by('-count')[:5])
    
    # Top equipment owners
    top_owners = list(User.objects.annotate(
        equipment_count=Count('equipment'),
        total_earned=Sum('equipment__rental__total_amount', filter=Q(equipment__rental__status='completed'))
    ).filter(equipment_count__gt=0).order_by('-total_earned')[:5])
    
    # Monthly revenue trend (last 12 months)
    monthly_revenue = []
    for i in range(12):
        month_start = today.replace(day=1) - timedelta(days=30*i)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        revenue = Rental.objects.filter(
            status='completed',
            created_at__date__range=[month_start, month_end]
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        monthly_revenue.append({
            'month': month_start.strftime('%Y-%m'),
            'revenue': float(revenue)
        })
    
    monthly_revenue.reverse()
    
    context = {
        'user_stats': user_stats,
        'equipment_stats': equipment_stats,
        'rental_stats': rental_stats,
        'top_categories': json.dumps(top_categories),
        'top_owners': top_owners,
        'monthly_revenue': json.dumps(monthly_revenue),
    }
    
    return render(request, 'admin/analytics.html', context)

@user_passes_test(lambda u: u.is_staff)
def admin_settings(request):
    """Admin settings and configuration"""
    
    if request.method == 'POST':
        # Handle settings updates here
        messages.success(request, 'Settings updated successfully.')
        return redirect('admin_settings')
    
    context = {
        # Add any site-wide settings here
    }
    
    return render(request, 'admin/settings.html', context)

@user_passes_test(lambda u: u.is_staff)
def admin_sensors(request):
    """Sensor management page"""
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    sensor_type_filter = request.GET.get('type', 'all')
    status_filter = request.GET.get('status', 'all')
    
    # Base queryset
    sensors = Sensor.objects.select_related('equipment').annotate(
        reading_count=Count('readings')
    )
    
    # Apply filters
    if search_query:
        sensors = sensors.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(equipment__title__icontains=search_query)
        )
    
    if sensor_type_filter != 'all':
        sensors = sensors.filter(sensor_type=sensor_type_filter)
    
    if status_filter != 'all':
        sensors = sensors.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(sensors.order_by('-created_at'), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_sensors = sensors.count()
    active_sensors = sensors.filter(status='active').count()
    online_sensors = sum(1 for sensor in sensors if sensor.is_online())
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'sensor_type_filter': sensor_type_filter,
        'status_filter': status_filter,
        'total_sensors': total_sensors,
        'active_sensors': active_sensors,
        'online_sensors': online_sensors,
        'sensor_types': Sensor.SENSOR_TYPES,
    }
    
    return render(request, 'admin/sensors.html', context)

@user_passes_test(lambda u: u.is_staff)
def admin_sensor_detail(request, sensor_id):
    """Individual sensor detail and management"""
    sensor = get_object_or_404(Sensor, id=sensor_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'toggle_active':
            sensor.is_active = not sensor.is_active
            sensor.save()
            status = 'activated' if sensor.is_active else 'deactivated'
            messages.success(request, f'Sensor {status} successfully.')
            
        elif action == 'update_status':
            new_status = request.POST.get('status')
            if new_status in dict(Sensor.STATUS_CHOICES):
                sensor.status = new_status
                sensor.save()
                messages.success(request, f'Sensor status updated to {new_status}.')
        
        return redirect('admin_sensor_detail', sensor_id=sensor.id)
    
    # Get sensor readings (last 50)
    sensor_readings = SensorReading.objects.filter(sensor=sensor).order_by('-timestamp')[:50]
    
    # Calculate statistics
    total_readings = sensor_readings.count()
    avg_quality = sensor_readings.aggregate(avg=Avg('quality_score'))['avg'] or 0
    
    context = {
        'sensor': sensor,
        'sensor_readings': sensor_readings,
        'total_readings': total_readings,
        'avg_quality': avg_quality,
    }
    
    return render(request, 'admin/sensor_detail.html', context)

@user_passes_test(lambda u: u.is_staff)
def admin_payment_initiation(request, rental_id):
    """Initiate payment for a rental from admin panel"""
    rental = get_object_or_404(Rental, id=rental_id)
    
    if request.method == 'POST':
        payment_type = request.POST.get('payment_type', 'rental_payment')
        
        # Initiate PayPal payment
        result = initiate_payment(rental, request)
        
        if result['success']:
            messages.success(request, 'Payment initiated successfully. Check the rental details for payment status.')
            return redirect('admin_rental_detail', rental_id=rental.id)
        else:
            messages.error(request, f'Failed to initiate payment: {result["error"]}')
    
    # Get existing payments for this rental
    payments = Payment.objects.filter(rental=rental).order_by('-created_at')
    
    context = {
        'rental': rental,
        'payments': payments,
        'payment_types': Payment.PAYMENT_TYPES,
    }
    
    return render(request, 'admin/payment_initiation.html', context)

@user_passes_test(lambda u: u.is_staff)
def admin_payments(request):
    """Payment management page"""
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', 'all')
    payment_method_filter = request.GET.get('method', 'all')
    
    # Base queryset
    payments = Payment.objects.select_related('rental', 'payer', 'rental__equipment')
    
    # Apply filters
    if search_query:
        payments = payments.filter(
            Q(rental__equipment__title__icontains=search_query) |
            Q(payer__username__icontains=search_query) |
            Q(paypal_order_id__icontains=search_query)
        )
    
    if status_filter != 'all':
        payments = payments.filter(status=status_filter)
    
    if payment_method_filter != 'all':
        payments = payments.filter(payment_method=payment_method_filter)
    
    # Pagination
    paginator = Paginator(payments.order_by('-created_at'), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_payments = payments.count()
    total_amount = payments.filter(status='completed').aggregate(total=Sum('amount'))['total'] or 0
    pending_payments = payments.filter(status='pending').count()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'payment_method_filter': payment_method_filter,
        'total_payments': total_payments,
        'total_amount': total_amount,
        'pending_payments': pending_payments,
        'payment_statuses': Payment.STATUS_CHOICES,
        'payment_methods': Payment.PAYMENT_METHOD_CHOICES,
    }
    
    return render(request, 'admin/payments.html', context)

@user_passes_test(lambda u: u.is_staff)
def admin_payment_detail(request, payment_id):
    """Individual payment detail and management"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'mark_completed':
            payment.status = 'completed'
            payment.save()
            messages.success(request, 'Payment marked as completed.')
            
        elif action == 'mark_failed':
            payment.status = 'failed'
            payment.save()
            messages.success(request, 'Payment marked as failed.')
            
        return redirect('admin_payment_detail', payment_id=payment.id)
    
    context = {
        'payment': payment,
    }
    
    return render(request, 'admin/payment_detail.html', context)
