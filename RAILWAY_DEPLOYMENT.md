# GameZone Railway + Render Deployment Guide

## 🚀 Deploy Django to Render with Railway Database

### Architecture
- **Backend**: Django on Render
- **Database**: PostgreSQL on Railway
- **Frontend**: (Optional) React/Next.js on Vercel

### Step 1: Set up Railway Database

1. **Go to Railway.app**
   - Visit: https://railway.app
   - Sign in with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Provision PostgreSQL"

3. **Configure Database**
   - **Name**: `gamezone-db`
   - **Region**: Choose closest to your users
   - Railway will automatically create a PostgreSQL database

4. **Get Database URL**
   - Go to your PostgreSQL service in Railway
   - Click "Connect" tab
   - Copy the "Postgres Connection URL"
   - It will look like: `postgresql://postgres:password@host:port/database`

### Step 2: Deploy Django to Render

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
   DATABASE_URL=your_railway_postgresql_url
   DEBUG=False
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_app_password
   PAYPAL_CLIENT_ID=your_paypal_client_id
   PAYPAL_CLIENT_SECRET=your_paypal_client_secret
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your Django app

### Step 3: Database Migration

1. **Automatic Migration**
   - Render will automatically run migrations during deployment
   - Or manually run: `python manage.py migrate`

2. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

### Step 4: Environment Variables Reference

| Variable | Description | Source |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Generate new one |
| `DATABASE_URL` | Railway PostgreSQL URL | Railway dashboard |
| `DEBUG` | Debug mode | Set to `False` |
| `EMAIL_HOST_USER` | Gmail address | Your Gmail |
| `EMAIL_HOST_PASSWORD` | Gmail app password | Gmail settings |
| `PAYPAL_CLIENT_ID` | PayPal client ID | PayPal developer |
| `PAYPAL_CLIENT_SECRET` | PayPal secret | PayPal developer |

### Step 5: Railway Database Benefits

✅ **Railway PostgreSQL**
- Free tier: 1GB storage, 1000 hours/month
- Automatic backups
- Easy scaling
- Built-in connection pooling

✅ **Render + Railway Integration**
- Seamless connection between services
- Environment variables automatically shared
- Automatic deployments

### Step 6: Testing the Connection

1. **Check Database Connection**
   - Go to Render logs
   - Look for successful database connection
   - Verify migrations ran successfully

2. **Test Admin Panel**
   - Visit: `https://your-app.onrender.com/admin/`
   - Login with superuser credentials

### Troubleshooting

1. **Database Connection Error**
   - Verify `DATABASE_URL` is correct
   - Check Railway database is running
   - Ensure network connectivity

2. **Migration Errors**
   - Check database permissions
   - Verify PostgreSQL extensions are available

3. **Environment Variables**
   - Double-check all variables are set in Render
   - Ensure no extra spaces or quotes

### Railway Database Configuration

Your Django settings are already configured for Railway:

```python
# In settings.py - already configured
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')
    )
}
```

### Next Steps

1. ✅ Set up Railway PostgreSQL database
2. ✅ Deploy Django to Render
3. ✅ Configure environment variables
4. ✅ Run migrations
5. ✅ Create superuser
6. ✅ Test the application

Your Django app will be available at: `https://your-app-name.onrender.com`
Database will be hosted on Railway with automatic backups and scaling. 