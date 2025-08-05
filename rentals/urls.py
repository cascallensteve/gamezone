from django.urls import path
from . import views
from . import admin_views
from . import auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/<uuid:equipment_id>/', views.equipment_detail, name='equipment_detail'),
    path('equipment/<uuid:equipment_id>/rent/', views.create_rental_request, name='create_rental_request'),
    path('load-more-equipment/', views.load_more_equipment, name='load_more_equipment'),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('about/', views.about, name='about'),
    
    # Authentication URLs
    path('accounts/login/', auth_views.CustomLoginView.as_view(), name='custom_login'),
    path('dashboard/', auth_views.DashboardView.as_view(), name='dashboard'),
    path('profile/', auth_views.profile_view, name='profile'),
    path('verify-email/<str:token>/', auth_views.verify_email, name='verify_email'),
    path('resend-verification/', auth_views.resend_verification, name='resend_verification'),
    path('switch-role/', auth_views.switch_role, name='switch_role'),
    
    # Existing views (updated to use new auth system)
    path('rental-requests/', views.rental_requests_dashboard, name='rental_requests_dashboard'),
    path('my-rentals/', views.my_rentals, name='my_rentals'),
    path('rental/<uuid:rental_id>/', views.rental_detail, name='rental_detail'),
    path('rental/<uuid:rental_id>/manage/', views.manage_rental, name='manage_rental'),
    path('list-equipment/', views.list_equipment, name='list_equipment'),
    path('my-equipment/', views.my_equipment, name='my_equipment'),
    path('equipment/<uuid:equipment_id>/edit/', views.edit_equipment, name='edit_equipment'),
    path('equipment/<uuid:equipment_id>/delete/', views.delete_equipment, name='delete_equipment'),
    path('equipment/<uuid:equipment_id>/toggle-status/', views.toggle_equipment_status, name='toggle_equipment_status'),
    #  Login URL
    path('admin-login/', views.admin_login, name='custom_admin_login'),
    path('admin-logout/', views.admin_logout, name='custom_admin_logout'),
    path('admin-panel/', views.custom_admin_dashboard, name='custom_admin_dashboard'),
    # Admin URLs
    path('admin-panel/users/', auth_views.AdminUserListView.as_view(), name='admin_users'),
    path('admin-panel/users/<int:pk>/', auth_views.AdminUserDetailView.as_view(), name='admin_user_detail'),
    path('admin-panel/users/<int:user_id>/action/', auth_views.admin_user_action, name='admin_user_action'),
    path('admin-panel/equipment/', admin_views.admin_equipment, name='admin_equipment'),
    path('admin-panel/equipment/<int:equipment_id>/', admin_views.admin_equipment_detail, name='admin_equipment_detail'),
    path('admin-panel/rentals/', admin_views.admin_rentals, name='admin_rentals'),
    path('admin-panel/rentals/<int:rental_id>/', admin_views.admin_rental_detail, name='admin_rental_detail'),
    path('admin-panel/categories/', admin_views.admin_categories, name='admin_categories'),
    path('admin-panel/analytics/', admin_views.admin_analytics, name='admin_analytics'),
    path('admin-panel/settings/', admin_views.admin_settings, name='admin_settings'),
    
    # New Admin URLs for Sensors and Payments
    path('admin-panel/sensors/', admin_views.admin_sensors, name='admin_sensors'),
    path('admin-panel/sensors/<uuid:sensor_id>/', admin_views.admin_sensor_detail, name='admin_sensor_detail'),
    path('admin-panel/payments/', admin_views.admin_payments, name='admin_payments'),
    path('admin-panel/payments/<uuid:payment_id>/', admin_views.admin_payment_detail, name='admin_payment_detail'),
    path('admin-panel/rentals/<uuid:rental_id>/initiate-payment/', admin_views.admin_payment_initiation, name='admin_payment_initiation'),
    
    # PayPal Payment URLs
    path('paypal/payment/success/<uuid:rental_id>/', views.paypal_payment_success, name='paypal_payment_success'),
    path('paypal/payment/cancel/<uuid:rental_id>/', views.paypal_payment_cancel, name='paypal_payment_cancel'),
]
