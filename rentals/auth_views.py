from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q, Count
from django.contrib.auth.views import LoginView
from .forms import (
    CustomSignupForm, CustomLoginForm, ProfileUpdateForm, 
    RoleChangeForm, AdminUserForm
)
from .models import CustomUser, UserProfile
import secrets
from django.utils import timezone

User = get_user_model()

class CustomLoginView(LoginView):
    """
    Custom login view to handle email authentication
    """
    form_class = CustomLoginForm
    template_name = 'account/login.html'
    
    def form_valid(self, form):
        """Log in the user and redirect to the next page."""
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, f'Welcome back, {user.first_name or user.username}! 🎮')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Handle invalid form submission."""
        messages.error(self.request, 'Invalid email or password. Please try again.')
        return super().form_invalid(form)

class DashboardView(TemplateView):
    """
    Main dashboard view with role-based content
    """
    template_name = 'rentals/dashboard.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context.update({
            'user_role': user.role,
            'is_customer': user.is_customer(),
            'is_vendor': user.is_vendor(),
            'is_admin': user.is_admin_user(),
        })
        
        # Add role-specific data
        if user.is_customer():
            context.update({
                'recent_rentals': user.rentals_as_renter.all()[:5],
                'wishlist_count': user.wishlist.count(),
            })
        elif user.is_vendor():
            context.update({
                'my_equipment': user.owned_equipment.all()[:5],
                'pending_requests': user.rentals_as_owner.filter(status='pending').count(),
                'active_rentals': user.rentals_as_owner.filter(status='active').count(),
            })
        elif user.is_admin_user():
            context.update({
                'total_users': User.objects.count(),
                'total_customers': User.objects.filter(role='customer').count(),
                'total_vendors': User.objects.filter(role='vendor').count(),
                'pending_verifications': User.objects.filter(is_email_verified=False).count(),
            })
        
        return context

@login_required
def profile_view(request):
    """
    User profile view and update
    """
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            form = ProfileUpdateForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('profile')
        elif 'change_role' in request.POST:
            role_form = RoleChangeForm(request.POST, instance=user)
            if role_form.is_valid():
                role_form.save()
                messages.success(request, f'Account type changed to {user.get_role_display()}!')
                return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user)
        role_form = RoleChangeForm(instance=user)
    
    context = {
        'form': form,
        'role_form': role_form,
        'profile': profile,
        'user': user,
    }
    return render(request, 'rentals/profile.html', context)

def verify_email(request, token):
    """
    Email verification view
    """
    try:
        user = User.objects.get(email_verification_token=token, is_email_verified=False)
        user.is_email_verified = True
        user.email_verification_token = ''
        user.save()
        
        # Auto-login the user after verification
        login(request, user)
        messages.success(request, 'Email verified successfully! Welcome to GameZone!')
        return redirect('dashboard')
    except User.DoesNotExist:
        messages.error(request, 'Invalid or expired verification link.')
        return redirect('account_signup')

@login_required
def resend_verification(request):
    """
    Resend email verification
    """
    user = request.user
    if user.is_email_verified:
        messages.info(request, 'Your email is already verified.')
        return redirect('dashboard')
    
    # Generate new token
    user.email_verification_token = secrets.token_urlsafe(50)
    user.save()
    
    # Send email with proper HTML formatting
    verification_url = request.build_absolute_uri(
        f'/verify-email/{user.email_verification_token}/'
    )
    
    subject = 'Verify your GameZone account'
    
    # HTML email content
    html_message = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Verify Your GameZone Account</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .button {{ display: inline-block; background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; font-weight: bold; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎮 GameZone</h1>
                <p>Welcome to the ultimate gaming equipment rental platform!</p>
            </div>
            <div class="content">
                <h2>Hi {user.first_name or user.username}!</h2>
                <p>Thank you for signing up with GameZone! We're excited to have you join our community of gamers.</p>
                
                <p>To complete your registration and start renting amazing gaming equipment, please verify your email address by clicking the button below:</p>
                
                <div style="text-align: center;">
                    <a href="{verification_url}" class="button">Verify Email Address</a>
                </div>
                
                <p>If the button doesn't work, you can also copy and paste this link into your browser:</p>
                <p style="word-break: break-all; background: #eee; padding: 10px; border-radius: 5px; font-size: 12px;">
                    {verification_url}
                </p>
                
                <p><strong>Important:</strong> This verification link will expire in 3 days for security reasons.</p>
                
                <p>If you didn't create this account, please ignore this email.</p>
            </div>
            <div class="footer">
                <p>Best regards,<br>The GameZone Team</p>
                <p>© 2025 GameZone. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    '''
    
    # Plain text fallback
    message = f'''
    Hi {user.first_name or user.username},
    
    Thank you for signing up with GameZone!
    
    Please click the link below to verify your email address:
    {verification_url}
    
    If you didn't create this account, please ignore this email.
    
    Best regards,
    The GameZone Team
    '''
    
    try:
        from django.core.mail import EmailMultiAlternatives
        email = EmailMultiAlternatives(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send()
        messages.success(request, 'Verification email sent successfully! Check your inbox.')
    except Exception as e:
        messages.error(request, f'Failed to send verification email: {str(e)}. Please try again.')
    
    return redirect('dashboard')

# Admin Views
def is_admin(user):
    return user.is_authenticated and (user.is_admin_user() or user.is_superuser)

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class AdminDashboardView(TemplateView):
    """
    Admin dashboard with system overview
    """
    template_name = 'rentals/admin/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # User statistics
        context.update({
            'total_users': User.objects.count(),
            'customers': User.objects.filter(role='customer').count(),
            'vendors': User.objects.filter(role='vendor').count(),
            'admins': User.objects.filter(role='admin').count(),
            'verified_users': User.objects.filter(is_email_verified=True).count(),
            'unverified_users': User.objects.filter(is_email_verified=False).count(),
            'recent_users': User.objects.order_by('-date_joined')[:10],
        })
        
        return context

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class AdminUserListView(ListView):
    """
    Admin view to list all users
    """
    model = User
    template_name = 'rentals/admin/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = User.objects.all().order_by('-date_joined')
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        
        # Filter by role
        role = self.request.GET.get('role')
        if role:
            queryset = queryset.filter(role=role)
        
        # Filter by verification status
        verified = self.request.GET.get('verified')
        if verified == 'true':
            queryset = queryset.filter(is_email_verified=True)
        elif verified == 'false':
            queryset = queryset.filter(is_email_verified=False)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search_query': self.request.GET.get('search', ''),
            'role_filter': self.request.GET.get('role', ''),
            'verified_filter': self.request.GET.get('verified', ''),
            'role_choices': User.ROLE_CHOICES,
        })
        return context

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class AdminUserDetailView(UpdateView):
    """
    Admin view to edit user details
    """
    model = User
    form_class = AdminUserForm
    template_name = 'rentals/admin/user_detail.html'
    success_url = reverse_lazy('admin_users')
    
    def form_valid(self, form):
        messages.success(self.request, f'User {form.instance.email} updated successfully!')
        return super().form_valid(form)

@login_required
@user_passes_test(is_admin)
def admin_user_action(request, user_id):
    """
    Handle admin actions on users (activate, deactivate, verify)
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    user = get_object_or_404(User, id=user_id)
    action = request.POST.get('action')
    
    if action == 'activate':
        user.is_active = True
        user.save()
        message = f'User {user.email} activated successfully!'
    elif action == 'deactivate':
        user.is_active = False
        user.save()
        message = f'User {user.email} deactivated successfully!'
    elif action == 'verify':
        user.is_email_verified = True
        user.save()
        message = f'User {user.email} verified successfully!'
    elif action == 'unverify':
        user.is_email_verified = False
        user.save()
        message = f'User {user.email} unverified successfully!'
    else:
        return JsonResponse({'error': 'Invalid action'}, status=400)
    
    messages.success(request, message)
    return JsonResponse({'success': True, 'message': message})

@login_required
def switch_role(request):
    """
    Allow users to switch between customer and vendor roles
    """
    if request.method == 'POST':
        new_role = request.POST.get('role')
        if new_role in ['customer', 'vendor']:
            request.user.role = new_role
            request.user.save()
            messages.success(request, f'Successfully switched to {new_role} mode!')
        else:
            messages.error(request, 'Invalid role selected.')
    
    return redirect('dashboard')
@login_required
def switch_role(request):
    """
    Allow users to switch between customer and vendor roles
    """
    if request.method == 'POST':
        new_role = request.POST.get('role')
        if new_role in ['customer', 'vendor']:
            request.user.role = new_role
            request.user.save()
            messages.success(request, f'Successfully switched to {new_role} mode!')
        else:
            messages.error(request, 'Invalid role selected.')
    
    return redirect('dashboard')

def admin_login_view(request):
    """
    Simple admin login view for admin/superuser only
    """
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('admin_dashboard')  # Redirect to custom admin panel
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and (user.is_staff or user.is_superuser):
            login(request, user)
            messages.success(request, f"Welcome, Administrator {user.get_full_name()}! 🔐")
            return redirect('admin_dashboard')  # Redirect to custom admin panel
        else:
            messages.error(request, "Access denied. Admin privileges required.")
    
    return render(request, 'admin/login.html')