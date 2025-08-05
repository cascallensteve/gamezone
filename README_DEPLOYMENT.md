# GameZone Vercel Deployment Guide

## Prerequisites

1. **GitHub Account**: Make sure your code is pushed to GitHub
2. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
3. **Database**: Set up a PostgreSQL database (recommended: Railway, Supabase, or Neon)
4. **Email Service**: Configure Gmail or other SMTP service for email verification

## Step 1: Prepare Your Repository

1. Make sure all files are committed to your GitHub repository
2. Ensure your repository structure looks like this:
   ```
   gamezone_env/
   ├── gamezone/
   │   ├── settings.py
   │   ├── urls.py
   │   └── wsgi.py
   ├── rentals/
   ├── requirements.txt
   ├── vercel.json
   └── build_files.sh
   ```

## Step 2: Set Up Database

### Option A: Railway (Recommended)
1. Go to [railway.app](https://railway.app)
2. Create a new project
3. Add a PostgreSQL database
4. Copy the database URL

### Option B: Supabase
1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Get the database connection string

### Option C: Neon
1. Go to [neon.tech](https://neon.tech)
2. Create a new project
3. Get the database connection string

## Step 3: Configure Email Service

### Gmail Setup
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
3. Use this password in your environment variables

## Step 4: Deploy to Vercel

### Method 1: Vercel Dashboard
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Configure the following settings:
   - **Framework Preset**: Other
   - **Root Directory**: `gamezone_env`
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Output Directory**: `staticfiles`
   - **Install Command**: `pip install -r requirements.txt`

### Method 2: Vercel CLI
1. Install Vercel CLI: `npm i -g vercel`
2. Navigate to your project directory
3. Run: `vercel`
4. Follow the prompts

## Step 5: Configure Environment Variables

In your Vercel project dashboard, go to Settings → Environment Variables and add:

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

## Step 6: Run Migrations

After deployment, you need to run migrations. You can do this via Vercel's function:

1. Create a migration function in your project
2. Or use Vercel's CLI: `vercel --prod`

## Step 7: Create Superuser

You can create a superuser by running:
```bash
vercel --prod -- python manage.py createsuperuser
```

## Troubleshooting

### Common Issues:

1. **Static Files Not Loading**
   - Make sure `whitenoise` is in your requirements.txt
   - Check that `STATIC_ROOT` is properly configured

2. **Database Connection Issues**
   - Verify your `DATABASE_URL` is correct
   - Make sure your database is accessible from Vercel's servers

3. **Email Not Sending**
   - Check your email credentials
   - Verify your Gmail app password is correct
   - Make sure 2FA is enabled on your Gmail account

4. **Migration Errors**
   - Run migrations manually using Vercel CLI
   - Check your database connection

### Debug Mode

For debugging, temporarily set:
```
DEBUG=True
```

## Post-Deployment Checklist

- [ ] Database migrations completed
- [ ] Superuser created
- [ ] Email verification working
- [ ] Static files loading correctly
- [ ] PayPal integration configured
- [ ] Custom domain configured (optional)

## Monitoring

- Use Vercel's built-in analytics
- Monitor your database performance
- Set up error tracking (optional)

## Security Notes

- Never commit sensitive information to your repository
- Use environment variables for all secrets
- Regularly rotate your secret keys
- Enable HTTPS in production

## Support

If you encounter issues:
1. Check Vercel's deployment logs
2. Verify all environment variables are set
3. Test your application locally first
4. Check the Django debug logs

Happy deploying! 🚀 