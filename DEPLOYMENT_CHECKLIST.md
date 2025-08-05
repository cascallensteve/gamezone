# 🚀 GameZone Deployment Checklist

## Pre-Deployment Checks

### ✅ Email Configuration
- [ ] Gmail 2FA enabled
- [ ] App password generated
- [ ] Email settings configured in Vercel environment variables
- [ ] Test email sending locally

### ✅ Database Setup
- [ ] PostgreSQL database created (Railway/Supabase/Neon)
- [ ] DATABASE_URL configured in Vercel
- [ ] Database accessible from Vercel servers

### ✅ Authentication
- [ ] Email verification working
- [ ] Login with email works
- [ ] Sign up sends verification email
- [ ] Login/logout toggle works correctly

## Deployment Steps

### 1. Push to GitHub
```bash
cd gamezone_env
git add .
git commit -m "Fix email verification and login issues"
git push origin main
```

### 2. Configure Vercel Environment Variables
```
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=postgresql://username:password@host:port/database
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret
PAYPAL_MODE=sandbox
SESSION_COOKIE_SECURE=True
```

### 3. Deploy to Vercel
- Go to [vercel.com](https://vercel.com)
- Import your GitHub repository
- Configure settings:
  - Framework: Other
  - Root Directory: `gamezone_env`
  - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
  - Output Directory: `staticfiles`

### 4. Post-Deployment Tasks
```bash
# Run migrations
vercel --prod -- python manage.py migrate

# Create superuser
vercel --prod -- python manage.py createsuperuser

# Test email sending
python test_email.py
```

## Testing Checklist

### ✅ Email Verification
- [ ] Sign up with new account
- [ ] Check email inbox for verification link
- [ ] Click verification link
- [ ] Verify account is marked as verified

### ✅ Login System
- [ ] Try logging in with email
- [ ] Verify login/logout toggle works
- [ ] Test with unverified account (should show error)
- [ ] Test with wrong password (should show error)

### ✅ Navigation
- [ ] Sign in button shows when logged out
- [ ] User menu shows when logged in
- [ ] Logout button works correctly
- [ ] Dashboard accessible after login

## Troubleshooting

### Email Not Sending
1. Check Gmail app password
2. Verify 2FA is enabled
3. Check environment variables in Vercel
4. Test with `python test_email.py`

### Login Not Working
1. Verify email verification is complete
2. Check if user exists in database
3. Verify password is correct
4. Check authentication backend settings

### Static Files Not Loading
1. Verify whitenoise is installed
2. Check STATIC_ROOT configuration
3. Run `python manage.py collectstatic`

## Success Indicators

✅ **Email verification emails are received in actual inbox**
✅ **Login works with email address**
✅ **Sign in button changes to logout when logged in**
✅ **All static files load correctly**
✅ **Database migrations completed**
✅ **Superuser can access admin panel**

## Support

If issues persist:
1. Check Vercel deployment logs
2. Verify all environment variables
3. Test locally first
4. Check Django debug logs

🎉 **Your GameZone app should now be fully functional!** 