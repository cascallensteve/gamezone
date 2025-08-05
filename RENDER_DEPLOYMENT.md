# GameZone Render Deployment Guide

## 🚀 Deploy Django to Render (Free & Easy)

### Step 1: Prepare Django for Production

Your Django project is already configured for Render deployment with:
- ✅ `gunicorn` for production server
- ✅ `whitenoise` for static files
- ✅ `dj-database-url` for database configuration
- ✅ `psycopg2-binary` for PostgreSQL support

### Step 2: Push to GitHub

Your project is already on GitHub:
- Repository: https://github.com/cascallensteve/terrys-project
- Branch: main

### Step 3: Deploy on Render

1. **Go to Render.com**
   - Visit: https://render.com
   - Sign in with GitHub

2. **Create New Web Service**
   - Click "New Web Service"
   - Connect your GitHub repository: `cascallensteve/terrys-project`

3. **Configure Service**
   - **Name**: `gamezone-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn gamezone.wsgi:application`

4. **Add Environment Variables**
   ```
   SECRET_KEY=your_django_secret_key_here
   DATABASE_URL=your_postgres_database_url
   DEBUG=False
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_app_password
   PAYPAL_CLIENT_ID=your_paypal_client_id
   PAYPAL_CLIENT_SECRET=your_paypal_client_secret
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your Django app

### Step 4: Database Setup

1. **Create PostgreSQL Database on Render**
   - Go to Render Dashboard
   - Click "New" → "PostgreSQL"
   - Name: `gamezone-db`
   - Copy the database URL

2. **Update Environment Variables**
   - Add the PostgreSQL URL to your web service environment variables
   - Set `DATABASE_URL` to the PostgreSQL connection string

3. **Run Migrations**
   - Render will automatically run migrations during deployment
   - Or manually run: `python manage.py migrate`

### Step 5: Static Files

Static files are automatically collected during build with:
```bash
python manage.py collectstatic --noinput
```

### Step 6: Create Admin User

After deployment, create a superuser:
```bash
python manage.py createsuperuser
```

### Step 7: Connect Frontend (if any)

If you have a React/Next.js frontend on Vercel:
- Set the API URL to your Render backend domain
- Use Axios or Fetch to call Django REST API

### Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `django-insecure-...` |
| `DATABASE_URL` | PostgreSQL connection | `postgresql://...` |
| `DEBUG` | Debug mode | `False` |
| `EMAIL_HOST_USER` | Gmail address | `your@gmail.com` |
| `EMAIL_HOST_PASSWORD` | Gmail app password | `app_password` |
| `PAYPAL_CLIENT_ID` | PayPal client ID | `your_paypal_id` |
| `PAYPAL_CLIENT_SECRET` | PayPal secret | `your_paypal_secret` |

### Troubleshooting

1. **Build Fails**
   - Check requirements.txt has all dependencies
   - Verify Python version compatibility

2. **Database Connection Error**
   - Ensure DATABASE_URL is correct
   - Check PostgreSQL service is running

3. **Static Files Not Loading**
   - Verify whitenoise is in MIDDLEWARE
   - Check STATIC_ROOT is set correctly

4. **500 Server Error**
   - Check Render logs for detailed error messages
   - Verify all environment variables are set

### Benefits of Render over Vercel for Django

✅ **Better Django Support**
- Native Python environment
- Proper WSGI server (gunicorn)
- PostgreSQL database support

✅ **Free Tier**
- 750 hours/month free
- PostgreSQL database included
- Automatic deployments

✅ **Easy Management**
- Simple dashboard
- Built-in logging
- Environment variable management

### Next Steps

1. Deploy to Render
2. Set up PostgreSQL database
3. Configure environment variables
4. Test the application
5. Connect frontend (if applicable)

Your Django app will be available at: `https://your-app-name.onrender.com` 