# 🚀 GameZone Render Deployment Guide

## Deploy Django to Render with Railway Database

### Architecture
- **Backend**: Django on Render
- **Database**: PostgreSQL on Railway
- **Domain**: `https://your-app-name.onrender.com`

### Step 1: Push to GitHub (if not done)

```bash
cd gamezone_env
git add .
git commit -m "Prepare Django for Render deployment"
git push origin main
```

### Step 2: Deploy to Render

1. **Go to Render.com**
   - Visit: https://render.com
   - Sign in with GitHub

2. **Create New Web Service**
   - Click "New Web Service"
   - Connect your GitHub repository: `cascallensteve/terrys-project`

3. **Configure Service Settings**
   - **Name**: `gamezone-backend`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: `gamezone_env`

4. **Build & Deploy Settings**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn gamezone.wsgi:application`

5. **Add Environment Variables**
   ```
   DATABASE_URL=postgresql://postgres:katCPTjldlGiZuNxYMZhwlSxPrHZEzaJ@centerbeam.proxy.rlwy.net:21318/railway
   SECRET_KEY=your-django-secret-key-here
   DEBUG=False
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   PAYPAL_CLIENT_ID=your-paypal-client-id
   PAYPAL_CLIENT_SECRET=your-paypal-client-secret
   ```

6. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your Django app

### Step 3: Post-Deployment Tasks

1. **Check Build Logs**
   - Go to your Render dashboard
   - Click on your service
   - Check "Logs" tab for any errors

2. **Run Migrations**
   - Render will automatically run migrations
   - Or manually run: `python manage.py migrate`

3. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

4. **Test Your App**
   - Visit: `https://your-app-name.onrender.com`
   - Test admin panel: `/admin/`
   - Test user registration and login

### Step 4: Environment Variables Reference

| Variable | Value | Description |
|----------|-------|-------------|
| `DATABASE_URL` | `postgresql://postgres:katCPTjldlGiZuNxYMZhwlSxPrHZEzaJ@centerbeam.proxy.rlwy.net:21318/railway` | Railway PostgreSQL |
| `SECRET_KEY` | `your-secret-key` | Django secret key |
| `DEBUG` | `False` | Production debug mode |
| `EMAIL_HOST_USER` | `your-email@gmail.com` | Gmail address |
| `EMAIL_HOST_PASSWORD` | `your-app-password` | Gmail app password |
| `PAYPAL_CLIENT_ID` | `your-paypal-id` | PayPal client ID |
| `PAYPAL_CLIENT_SECRET` | `your-paypal-secret` | PayPal secret |

### Step 5: Render Features

✅ **Free Tier Benefits**
- 750 hours/month free
- Automatic deployments
- Built-in SSL certificates
- Custom domains support

✅ **Django Optimizations**
- Automatic static file collection
- Gunicorn WSGI server
- Environment variable management
- Real-time logs

✅ **Database Integration**
- Seamless Railway PostgreSQL connection
- SSL encryption
- Automatic connection pooling

### Step 6: Troubleshooting

1. **Build Fails**
   - Check requirements.txt has all dependencies
   - Verify Python version compatibility
   - Check build logs for specific errors

2. **Database Connection Error**
   - Verify DATABASE_URL is correct
   - Check Railway database is running
   - Ensure SSL connection is working

3. **Static Files Not Loading**
   - Verify whitenoise is in MIDDLEWARE
   - Check STATIC_ROOT is set correctly
   - Ensure collectstatic ran successfully

4. **500 Server Error**
   - Check Render logs for detailed error messages
   - Verify all environment variables are set
   - Test database connection

### Step 7: Monitoring & Maintenance

1. **Check Logs**
   - Render dashboard → Your service → Logs
   - Monitor for errors and performance

2. **Database Monitoring**
   - Railway dashboard → Your database
   - Check connection status and usage

3. **Performance**
   - Monitor response times
   - Check database query performance
   - Optimize as needed

### Step 8: Custom Domain (Optional)

1. **Add Custom Domain**
   - Render dashboard → Your service → Settings
   - Add your domain name
   - Update DNS records

2. **SSL Certificate**
   - Render provides automatic SSL
   - No additional configuration needed

### Success Checklist

- [ ] GitHub repository pushed
- [ ] Render service created
- [ ] Environment variables set
- [ ] Build successful
- [ ] Database migrations run
- [ ] Superuser created
- [ ] Admin panel accessible
- [ ] User registration working
- [ ] Email sending configured
- [ ] PayPal integration (if needed)

### Your App URL
After deployment, your app will be available at:
`https://your-app-name.onrender.com`

Replace `your-app-name` with the name you chose for your Render service. 