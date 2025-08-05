# GameZone Deployment Guide

## Database Migration to Production (Supabase)

### Current Status
✅ **Development Setup Complete**
- Custom User Model with roles (Customer, Vendor, Admin)
- Authentication system with email verification
- Admin interface
- All migrations created and tested locally

### Production Database Setup

#### 1. Network Connectivity
The Supabase connection requires internet access. Current error suggests:
```
could not translate host name "db.wjufiadtiukmdpxlqcjb.supabase.co" to address
```

**Solutions:**
- Ensure internet connectivity
- Check firewall settings
- Verify DNS resolution

#### 2. Supabase Configuration
**Database Details:**
- Host: `db.wjufiadtiukmdpxlqcjb.supabase.co`
- Port: `5432`
- Database: `postgres`
- User: `postgres`
- Password: `Stevoh@Stevh2020`

#### 3. Production Migration Commands
Once connectivity is established:

```bash
# Navigate to project directory
cd "C:\Users\user\OneDrive\Desktop\New folder\Gameszone\gamezone_env"

# Run migrations to Supabase
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files (for production)
python manage.py collectstatic

# Start server
python manage.py runserver
```

### Current Working Setup (Development)
For immediate testing and development, the system is configured with SQLite and can be switched back:

```python
# In settings.py, uncomment this for local development:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Email Configuration
Update these settings in `settings.py` for email verification:

```python
EMAIL_HOST_USER = 'your-gmail@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Gmail App Password
DEFAULT_FROM_EMAIL = 'your-gmail@gmail.com'
```

### Testing the System

#### Authentication Features:
1. **User Registration:** `/accounts/signup/`
   - Email verification required
   - Role selection (Customer/Vendor)
   - Phone number optional

2. **User Login:** `/accounts/login/`
   - Email-based authentication
   - Rate limiting protection
   - Session management

3. **Dashboard:** `/dashboard/`
   - Role-based content
   - Customer: Recent rentals, wishlist
   - Vendor: Equipment management, rental requests
   - Admin: System overview, user management

4. **Admin Panel:** `/admin-panel/`
   - Custom admin interface
   - User management with actions
   - System analytics

5. **Profile Management:** `/profile/`
   - Update personal information
   - Change account type (Customer ↔ Vendor)

### Production Checklist
- [ ] Verify internet connectivity to Supabase
- [ ] Update email settings with real SMTP credentials
- [ ] Run production migrations
- [ ] Create admin superuser
- [ ] Test all authentication flows
- [ ] Configure production static files serving
- [ ] Set DEBUG = False for production
- [ ] Configure ALLOWED_HOSTS for production domain

### Security Features Implemented
✅ Email verification mandatory
✅ Password strength validation
✅ Login attempt rate limiting
✅ CSRF protection
✅ Session security
✅ Role-based access control
✅ Admin user verification

### Next Steps
1. **Fix network connectivity** to migrate to Supabase
2. **Configure email service** for OTP verification
3. **Test complete authentication flow**
4. **Deploy to production server**
5. **Implement M-Pesa payment integration**
