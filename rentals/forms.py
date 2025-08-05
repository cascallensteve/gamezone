from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Div
from crispy_forms.bootstrap import FormActions
import secrets

User = get_user_model()

class CustomSignupForm(SignupForm):
    """
    Custom signup form with role selection and phone number
    """
    ROLE_CHOICES = [
        ('customer', 'Customer - Rent gaming equipment'),
        ('vendor', 'Vendor - Rent out my gaming equipment'),
        ('admin', 'Admin - System administrator'),
    ]
    
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, widget=forms.RadioSelect)
    phone_number = forms.CharField(max_length=15, required=False)
    terms_accepted = forms.BooleanField(
        required=True,
        label="I agree to the Terms of Service and Privacy Policy"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h3 class="text-center mb-4">Create Your GameZone Account</h3>'),
            Row(
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name', css_class='form-group col-md-6'),
            ),
            'email',
            Row(
                Column('password1', css_class='form-group col-md-6'),
                Column('password2', css_class='form-group col-md-6'),
            ),
            'phone_number',
            HTML('<div class="form-group">'),
            HTML('<label class="form-label">Account Type</label>'),
            'role',
            HTML('</div>'),
            'terms_accepted',
            FormActions(
                Submit('signup', 'Create Account', css_class='btn btn-primary btn-lg w-100')
            )
        )
        
        # Add CSS classes to form fields
        self.fields['email'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Enter your email address'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Create a strong password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Confirm your password'
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'First name'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Last name'
        })
        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': '+1 (555) 123-4567'
        })
    
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        
        if role == 'admin':
            if email != 'admin@gamezone.com':
                raise forms.ValidationError("Admin email must be admin@gamezone.com")
            if password1 != 'GZ!SuperSecure2024$':
                raise forms.ValidationError("Admin password must be GZ!SuperSecure2024$")
            # Remove password validation errors for admin
            self._errors.pop('password1', None)
            self._errors.pop('password2', None)
        
        return cleaned_data
    
    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = self.cleaned_data['role']
        user.phone_number = self.cleaned_data['phone_number']
        user.email_verification_token = secrets.token_urlsafe(50)
        
        # Set admin details if role is admin
        if user.role == 'admin':
            user.username = 'admin'
            user.first_name = 'Admin'
            user.last_name = 'User'
            user.is_staff = True
            user.is_superuser = True
            user.is_email_verified = True
        else:
            # Send verification email for non-admin users
            self.send_verification_email(request, user)
        
        user.save()
        return user
    
    def send_verification_email(self, request, user):
        """
        Send verification email to the user
        """
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
            from django.conf import settings
            email = EmailMultiAlternatives(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email]
            )
            email.attach_alternative(html_message, "text/html")
            email.send()
        except Exception as e:
            # Log the error but don't fail the signup
            print(f"Failed to send verification email: {str(e)}")

class CustomLoginForm(AuthenticationForm):
    """
    Custom login form with enhanced styling
    """
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your email address'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h3 class="text-center mb-4">Welcome Back to GameZone</h3>'),
            'username',
            'password',
            Div(
                HTML('<a href="{% url \'account_reset_password\' %}" class="text-primary">Forgot Password?</a>'),
                css_class='text-end mb-3'
            ),
            FormActions(
                Submit('login', 'Sign In', css_class='btn btn-primary btn-lg w-100 mb-3')
            ),
            HTML('''
                <div class="text-center">
                    <p>Don't have an account? <a href="{% url 'account_signup' %}" class="text-primary">Sign up here</a></p>
                </div>
            ''')
        )
        
        self.fields['password'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Enter your password'
        })
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('username')  # username field contains email
        password = cleaned_data.get('password')
        
        if email and password:
            # Try to authenticate with email
            from django.contrib.auth import authenticate
            user = authenticate(username=email, password=password)
            
            if user is None:
                # Try to find user by email and authenticate
                try:
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    user_obj = User.objects.get(email=email)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user is None:
                raise forms.ValidationError(
                    "Invalid email or password. Please try again."
                )
            elif not user.is_active:
                raise forms.ValidationError(
                    "This account is inactive. Please contact support."
                )
            elif not user.is_email_verified:
                raise forms.ValidationError(
                    "Please verify your email address before logging in. "
                    "Check your inbox for the verification link."
                )
            else:
                cleaned_data['user'] = user
        
        return cleaned_data

class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h4>Update Profile Information</h4>'),
            Row(
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name', css_class='form-group col-md-6'),
            ),
            'phone_number',
            FormActions(
                Submit('update', 'Update Profile', css_class='btn btn-primary')
            )
        )
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class RoleChangeForm(forms.ModelForm):
    """
    Form for users to change their role (customer/vendor)
    """
    ROLE_CHOICES = [
        ('customer', 'Customer - Rent gaming equipment'),
        ('vendor', 'Vendor - Rent out my gaming equipment'),
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)
    
    class Meta:
        model = User
        fields = ['role']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h4>Change Account Type</h4>'),
            HTML('<p class="text-muted">You can switch between customer and vendor modes at any time.</p>'),
            'role',
            FormActions(
                Submit('change_role', 'Update Account Type', css_class='btn btn-warning')
            )
        )

class AdminUserForm(forms.ModelForm):
    """
    Admin form for creating/editing users
    """
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'role', 'phone_number', 
                 'is_active', 'is_staff', 'is_superuser', 'is_email_verified']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h4>User Management</h4>'),
            Row(
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name', css_class='form-group col-md-6'),
            ),
            Row(
                Column('email', css_class='form-group col-md-6'),
                Column('username', css_class='form-group col-md-6'),
            ),
            Row(
                Column('role', css_class='form-group col-md-6'),
                Column('phone_number', css_class='form-group col-md-6'),
            ),
            HTML('<h5>Permissions</h5>'),
            Row(
                Column('is_active', css_class='form-group col-md-3'),
                Column('is_staff', css_class='form-group col-md-3'),
                Column('is_superuser', css_class='form-group col-md-3'),
                Column('is_email_verified', css_class='form-group col-md-3'),
            ),
            FormActions(
                Submit('save', 'Save User', css_class='btn btn-success')
            )
        )
        
        for field in self.fields:
            if field not in ['is_active', 'is_staff', 'is_superuser', 'is_email_verified']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})


# Equipment Forms
class EquipmentForm(forms.ModelForm):
    """
    Form for creating and editing equipment
    """
    class Meta:
        from .models import Equipment
        model = Equipment
        fields = [
            'title', 'description', 'category', 'brand', 'model', 
            'year_purchased', 'condition', 'daily_rate', 'weekly_rate', 
            'monthly_rate', 'security_deposit', 'is_available_for_pickup',
            'is_available_for_delivery', 'delivery_radius_km', 'delivery_fee',
            'location_city', 'location_state', 'included_accessories',
            'usage_instructions', 'special_requirements'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'included_accessories': forms.Textarea(attrs={'rows': 3}),
            'usage_instructions': forms.Textarea(attrs={'rows': 3}),
            'special_requirements': forms.Textarea(attrs={'rows': 3}),
            'year_purchased': forms.NumberInput(attrs={'min': 1980, 'max': 2024}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h4>Equipment Details</h4>'),
            Row(
                Column('title', css_class='form-group col-md-8'),
                Column('category', css_class='form-group col-md-4'),
            ),
            'description',
            Row(
                Column('brand', css_class='form-group col-md-6'),
                Column('model', css_class='form-group col-md-6'),
            ),
            Row(
                Column('year_purchased', css_class='form-group col-md-6'),
                Column('condition', css_class='form-group col-md-6'),
            ),
            HTML('<h5>Pricing</h5>'),
            Row(
                Column('daily_rate', css_class='form-group col-md-4'),
                Column('weekly_rate', css_class='form-group col-md-4'),
                Column('monthly_rate', css_class='form-group col-md-4'),
            ),
            'security_deposit',
            HTML('<h5>Availability & Location</h5>'),
            Row(
                Column('is_available_for_pickup', css_class='form-group col-md-6'),
                Column('is_available_for_delivery', css_class='form-group col-md-6'),
            ),
            Row(
                Column('delivery_radius_km', css_class='form-group col-md-6'),
                Column('delivery_fee', css_class='form-group col-md-6'),
            ),
            Row(
                Column('location_city', css_class='form-group col-md-6'),
                Column('location_state', css_class='form-group col-md-6'),
            ),
            HTML('<h5>Additional Information</h5>'),
            'included_accessories',
            'usage_instructions',
            'special_requirements',
            FormActions(
                Submit('save', 'Save Equipment', css_class='btn btn-primary btn-lg')
            )
        )
        
        # Add CSS classes to form fields
        for field in self.fields:
            if field not in ['is_available_for_pickup', 'is_available_for_delivery']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})

class EquipmentImageForm(forms.ModelForm):
    """
    Form for uploading equipment images
    """
    class Meta:
        from .models import EquipmentImage
        model = EquipmentImage
        fields = ['image', 'caption', 'is_primary']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'image',
            'caption',
            'is_primary',
            FormActions(
                Submit('upload', 'Upload Image', css_class='btn btn-success')
            )
        )
        
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['caption'].widget.attrs.update({'class': 'form-control'})

class EquipmentFilterForm(forms.Form):
    """
    Form for filtering equipment listings
    """
    CONDITION_CHOICES = [
        ('', 'Any Condition'),
        ('excellent', 'Excellent'),
        ('very_good', 'Very Good'),
        ('good', 'Good'),
        ('fair', 'Fair'),
    ]
    
    SORT_CHOICES = [
        ('newest', 'Newest First'),
        ('oldest', 'Oldest First'),
        ('price_low', 'Price: Low to High'),
        ('price_high', 'Price: High to Low'),
        ('rating', 'Highest Rated'),
    ]
    
    search = forms.CharField(
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search equipment...',
            'class': 'form-control'
        })
    )
    category = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    condition = forms.ChoiceField(
        choices=CONDITION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    min_price = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min price'
        })
    )
    max_price = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max price'
        })
    )
    location = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'City or State',
            'class': 'form-control'
        })
    )
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial='newest',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    available_for_pickup = forms.BooleanField(required=False)
    available_for_delivery = forms.BooleanField(required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import EquipmentCategory
        self.fields['category'].queryset = EquipmentCategory.objects.filter(is_active=True)
