#!/bin/bash

echo "🚀 GameZone Vercel Deployment Script"
echo "====================================="

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
    echo "   git remote add origin https://github.com/yourusername/yourrepo.git"
    exit 1
fi

echo "✅ Git repository found"

# Push to GitHub
echo "📤 Pushing to GitHub..."
git add .
git commit -m "Deploy to Vercel - $(date)"
git push origin main

echo "✅ Code pushed to GitHub"
echo ""
echo "🎯 Next Steps:"
echo "1. Go to https://vercel.com"
echo "2. Click 'New Project'"
echo "3. Import your GitHub repository"
echo "4. Configure settings:"
echo "   - Framework Preset: Other"
echo "   - Root Directory: gamezone_env"
echo "   - Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput"
echo "   - Output Directory: staticfiles"
echo "5. Add environment variables in Vercel dashboard"
echo "6. Deploy!"
echo ""
echo "📖 See README_DEPLOYMENT.md for detailed instructions" 