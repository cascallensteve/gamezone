#!/bin/bash

echo "🚀 GameZone Render Deployment Script"
echo "===================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

# Check if remote is set
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ No remote repository found. Please add your GitHub repository:"
    echo "   git remote add origin https://github.com/cascallensteve/terrys-project.git"
    exit 1
fi

echo "✅ Git repository found"

# Push to GitHub
echo "📤 Pushing to GitHub..."
git add .
git commit -m "Deploy to Render - $(date)"
git push origin main

echo "✅ Code pushed to GitHub"
echo ""
echo "🎯 Next Steps:"
echo "1. Go to https://render.com"
echo "2. Click 'New Web Service'"
echo "3. Connect your GitHub repository: cascallensteve/terrys-project"
echo "4. Configure settings:"
echo "   - Name: gamezone-backend"
echo "   - Environment: Python 3"
echo "   - Root Directory: gamezone_env"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: gunicorn gamezone.wsgi:application"
echo "5. Add environment variables:"
echo "   DATABASE_URL=postgresql://postgres:katCPTjldlGiZuNxYMZhwlSxPrHZEzaJ@centerbeam.proxy.rlwy.net:21318/railway"
echo "   SECRET_KEY=your-secret-key"
echo "   DEBUG=False"
echo "   EMAIL_HOST_USER=your-email@gmail.com"
echo "   EMAIL_HOST_PASSWORD=your-app-password"
echo "6. Deploy!"
echo ""
echo "📖 See RENDER_DEPLOYMENT_GUIDE.md for detailed instructions" 