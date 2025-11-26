# 🚂 Railway Deployment Guide - ReadWise Backend

## Why Railway?

✅ **No timeout limits** - Perfect for AI background processing  
✅ **Free tier available** - $5 free credit monthly  
✅ **Simple deployment** - Deploy from GitHub or CLI  
✅ **Auto-deployments** - Auto-deploys on git push  
✅ **Built-in database** - Can provision PostgreSQL if needed  

---

## 📋 Prerequisites

- GitHub account
- Railway account (sign up at [railway.app](https://railway.app))
- Your code pushed to GitHub

---

## 🚀 Deployment Methods

### **Method 1: Deploy from GitHub (Recommended)**

#### Step 1: Push Your Code to GitHub

```bash
cd /home/hushrama/Desktop/Fastapi\ Projs/read-wise/backend

# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Ready for Railway deployment"

# Add your GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git push -u origin main
```

#### Step 2: Deploy on Railway

1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository
5. Railway will automatically detect it's a Python project
6. Click **"Deploy"**

#### Step 3: Add Environment Variables

1. In your Railway project, click on your service
2. Go to **"Variables"** tab
3. Click **"New Variable"** and add these one by one:

```
DATABASE_URL=<your-supabase-connection-string>
SUPABASE_JWT_SECRET=WG2aDlX5D8wdkdxCFTWQRNhsJk3jCns4Kl8I/l/WtdfIX1b8ZhNqOAYf/EBfWSd+j5FbXforL0dij18/xXmU7w==
OPENAI_API_KEY=<your-openai-api-key>
```

**Important for DATABASE_URL:**
- Use Supabase's **regular connection string** (port 5432), NOT pooling
- Railway supports persistent connections
- Get it from: Supabase Dashboard → Settings → Database → Connection String → URI

#### Step 4: Generate Domain

1. Go to **"Settings"** tab
2. Under **"Networking"**, click **"Generate Domain"**
3. Your API will be available at: `https://your-app.up.railway.app`

#### Step 5: Verify Deployment

```bash
# Test health endpoint
curl https://your-app.up.railway.app/health

# Expected response:
# {"status": "ok"}
```

---

### **Method 2: Deploy Using Railway CLI**

#### Step 1: Install Railway CLI

```bash
# Using npm
npm i -g @railway/cli

# Or using curl
curl -fsSL https://railway.app/install.sh | sh
```

#### Step 2: Login to Railway

```bash
railway login
```

This will open a browser window to authenticate.

#### Step 3: Initialize Railway Project

```bash
cd /home/hushrama/Desktop/Fastapi\ Projs/read-wise/backend

railway init
```

Follow the prompts:
- Choose **"Create new project"**
- Give it a name (e.g., "readwise-backend")

#### Step 4: Link to Your Project

```bash
railway link
```

#### Step 5: Add Environment Variables

```bash
# Add variables one by one
railway variables set DATABASE_URL="<your-supabase-url>"
railway variables set SUPABASE_JWT_SECRET="WG2aDlX5D8wdkdxCFTWQRNhsJk3jCns4Kl8I/l/WtdfIX1b8ZhNqOAYf/EBfWSd+j5FbXforL0dij18/xXmU7w=="
railway variables set OPENAI_API_KEY="<your-openai-key>"
```

#### Step 6: Deploy

```bash
railway up
```

This will:
- Upload your code
- Install dependencies
- Start the server

#### Step 7: Open Your App

```bash
railway open
```

This opens your deployed app in the browser.

---

## 🔗 Getting Your Supabase Database URL

### For Railway (Use Standard Connection String)

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project
3. Go to **Settings** → **Database**
4. Under **"Connection string"**, select **"URI"**
5. Copy the connection string (should look like):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres
   ```
6. Replace `[YOUR-PASSWORD]` with your actual database password

**Don't use connection pooling for Railway** - Railway handles connections better with the standard connection string.

---

## 🔧 Configuration Files Created

- ✅ `Procfile` - Tells Railway how to start your app
- ✅ `railway.json` - Railway-specific configuration
- ✅ `runtime.txt` - Specifies Python version

---

## 🔄 Auto-Deployments (GitHub Method)

Once deployed from GitHub:
1. Every time you push to `main` branch
2. Railway automatically rebuilds and redeploys
3. Zero downtime deployments

To deploy updates:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

Railway will automatically deploy! 🎉

---

## 💰 Railway Pricing

### Free Tier
- **$5 free credit per month**
- About **500 hours** of runtime for a small app
- Perfect for development and small projects

### Paid Usage
- **$0.000231/GB-hour** for memory
- **$0.000463/vCPU-hour** for CPU
- Typically costs **$5-$10/month** for a production app

---

## 🎯 Post-Deployment Checklist

1. ✅ Verify health endpoint works
2. ✅ Test book upload with JWT token
3. ✅ Check Railway logs for errors:
   ```bash
   railway logs
   ```
4. ✅ Update CORS in `main.py` with your frontend URL:
   ```python
   allow_origins=["https://your-frontend.vercel.app"]
   ```
5. ✅ Redeploy after CORS update:
   ```bash
   git add .
   git commit -m "Update CORS"
   git push
   ```

---

## 📊 Monitoring

### View Logs
```bash
# Via CLI
railway logs

# Or in Railway dashboard
# Project → Service → Deployments → Click on deployment → Logs
```

### View Metrics
- In Railway dashboard, go to **"Metrics"** tab
- See CPU, Memory, Network usage

---

## 🐛 Troubleshooting

### "Application failed to respond"
- Check logs: `railway logs`
- Verify environment variables are set
- Make sure port is set to `$PORT` (Railway provides this)

### "Database connection failed"
- Ensure DATABASE_URL is correct
- Use standard connection string (port 5432), not pooling
- Check Supabase database password

### "Module not found"
- Ensure `requirements.txt` includes all dependencies
- Railway auto-installs from `requirements.txt`

### "502 Bad Gateway"
- App might be starting up (wait 30 seconds)
- Check logs for Python errors
- Verify uvicorn is starting correctly

---

## 🔐 Security Best Practices

1. **Never commit `.env` file** (already in `.gitignore`)
2. **Use Railway's environment variables** for secrets
3. **Enable CORS only for your frontend domain** (not `*`)
4. **Keep dependencies updated**

---

## 📚 Useful Railway Commands

```bash
# View logs
railway logs

# Open dashboard
railway open

# Run commands in Railway environment
railway run python manage.py migrate

# View environment variables
railway variables

# Link to different project
railway link

# Unlink from project
railway unlink

# Get help
railway help
```

---

## 🎉 You're Done!

Your backend is now deployed on Railway with:
- ✅ No timeout limits for AI processing
- ✅ Auto-deployments from GitHub
- ✅ Production-ready infrastructure
- ✅ Easy monitoring and logs

**Next step:** Get your Railway URL and use it in your frontend! 🚀
