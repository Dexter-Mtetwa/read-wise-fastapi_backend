# 🚂 Quick Railway Deploy - Step by Step

## Choose Your Method:

---

## 🎯 **Method 1: GitHub (Easiest - Recommended)**

### 1️⃣ Push to GitHub

```bash
cd /home/hushrama/Desktop/Fastapi\ Projs/read-wise/backend

# Check if git is initialized
git status

# If not initialized:
git init

# Add all files
git add .

# Commit
git commit -m "Ready for Railway deployment"

# Add your GitHub remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push
git push -u origin main
```

### 2️⃣ Deploy on Railway

1. Go to **[railway.app](https://railway.app)**
2. Sign up/Login (use GitHub account for easier integration)
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your `readwise-backend` repository
6. Railway will auto-detect Python and deploy!

### 3️⃣ Add Environment Variables

In Railway dashboard:
1. Click on your deployed service
2. Go to **"Variables"** tab
3. Click **"+ New Variable"**
4. Add these three variables:

```
DATABASE_URL
SUPABASE_JWT_SECRET
OPENAI_API_KEY
```

**Copy from your `.env` file!**

### 4️⃣ Generate Public URL

1. Go to **"Settings"** tab
2. Under **"Networking"**, click **"Generate Domain"**
3. Copy your URL: `https://your-app.up.railway.app`

### 5️⃣ Test It!

```bash
curl https://your-app.up.railway.app/health
```

✅ **You're done!** Use this URL in your frontend.

---

## 🖥️ **Method 2: Railway CLI**

### 1️⃣ Install Railway CLI

```bash
npm install -g @railway/cli
```

### 2️⃣ Login

```bash
railway login
```

Browser will open for authentication.

### 3️⃣ Initialize & Deploy

```bash
cd /home/hushrama/Desktop/Fastapi\ Projs/read-wise/backend

# Create new project
railway init

# Set environment variables
railway variables set DATABASE_URL="paste-from-env"
railway variables set SUPABASE_JWT_SECRET="paste-from-env"
railway variables set OPENAI_API_KEY="paste-from-env"

# Deploy!
railway up

# Generate public URL (in Railway dashboard or):
railway domain
```

### 4️⃣ Get Your URL

```bash
railway open
```

---

## 📋 What You Need Ready

Before deploying, make sure you have:

✅ **GitHub account** (for Method 1)  
✅ **Supabase database URL** (from your `.env`)  
✅ **Supabase JWT Secret** (from your `.env`)  
✅ **OpenAI API Key** (from your `.env`)  

---

## 🎯 After Deployment

1. **Get your Railway URL** (e.g., `https://readwise-backend.up.railway.app`)

2. **Test the health endpoint:**
   ```bash
   curl https://your-url.up.railway.app/health
   ```

3. **Update CORS** in `main.py` with your frontend URL:
   ```python
   allow_origins=["https://your-frontend.vercel.app"],
   ```

4. **Redeploy** (automatic if using GitHub, or run `railway up` if using CLI)

5. **Use this URL in your frontend!**

---

## 💡 Tips

- **GitHub method = auto-deployments** (every `git push` redeploys)
- **CLI method = manual deployments** (run `railway up` to deploy)
- **Logs**: `railway logs` or check in Railway dashboard
- **Free tier**: $5/month credit (enough for development)

---

## 🆘 Need Help?

Check `RAILWAY_DEPLOY.md` for detailed troubleshooting and advanced options.

---

**Ready to deploy? Choose your method and go! 🚀**
