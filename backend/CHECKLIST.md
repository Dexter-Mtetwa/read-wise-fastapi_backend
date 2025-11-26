# 🚀 Pre-Deployment Checklist - ReadWise Backend

## ✅ What We've Done

### 1. **CORS Configuration**
   - ✅ Added CORS middleware to `main.py`
   - ✅ Currently allows all origins (`*`)
   - ⚠️ Update with your frontend URL after deployment

### 2. **Vercel Configuration Files**
   - ✅ `vercel.json` - Vercel deployment settings
   - ✅ `index.py` - Entry point for Vercel
   - ✅ `.gitignore` - Prevents sensitive files from being committed

### 3. **Documentation**
   - ✅ `DEPLOYMENT.md` - Complete deployment guide
   - ✅ `AUTHENTICATION.md` - Authentication setup guide
   - ✅ `README.md` - Project overview

### 4. **Code Ready**
   - ✅ JWT authentication implemented
   - ✅ Row Level Security (RLS) support with `owner_id`
   - ✅ All dependencies in `requirements.txt`

---

## ⚠️ CRITICAL: Vercel Hobby Plan Limitation

**Your backend has AI processing that runs in the background.** This might not work on Vercel Hobby because:

- ⏱️ **10-second timeout** on Hobby plan
- 🤖 **AI processing takes longer** than 10 seconds
- ❌ **Background tasks will fail**

### Recommended Solutions:

1. **Use Vercel Pro** ($20/month) - 60-second timeout
2. **Use Railway** (Free tier available) - No timeout limit
3. **Use Render** (Free tier available) - No timeout limit

**If you proceed with Vercel Hobby:**
- Initial upload will work
- Background AI processing might fail
- Users won't see summaries/questions

---

## 📋 Deployment Steps (Quick Version)

### Option A: Vercel (Recommended for API endpoints only)

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Initial backend setup"
git remote add origin <your-repo-url>
git push -u origin main

# 2. Go to vercel.com
# 3. Import your GitHub repo
# 4. Add environment variables:
#    - DATABASE_URL
#    - SUPABASE_JWT_SECRET  
#    - OPENAI_API_KEY
# 5. Deploy!
```

### Option B: Railway (Recommended if you want background tasks to work)

```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login and deploy
railway login
railway init
railway up

# 3. Add environment variables in Railway dashboard
```

---

## 🔑 Environment Variables to Set

When deploying, add these in your hosting dashboard:

```
DATABASE_URL=<your-supabase-connection-pooling-url>
SUPABASE_JWT_SECRET=WG2aDlX5D8wdkdxCFTWQRNhsJk3jCns4Kl8I/l/WtdfIX1b8ZhNqOAYf/EBfWSd+j5FbXforL0dij18/xXmU7w==
OPENAI_API_KEY=<your-openai-key>
```

**Get Supabase Connection Pooling URL:**
1. Supabase Dashboard → Settings → Database
2. Connection string → **Connection Pooling** (port 6543, not 5432)
3. Copy the full URL

---

## 🎯 After Deployment

1. Get your backend URL (e.g., `https://your-backend.vercel.app`)
2. Test health endpoint: `https://your-backend.vercel.app/health`
3. Update CORS in `main.py` with your frontend URL
4. Use this URL in your frontend

---

## 📦 Files Added/Modified

- ✅ `main.py` - Added CORS middleware
- ✅ `vercel.json` - Vercel configuration
- ✅ `index.py` - Vercel entry point
- ✅ `services/auth.py` - JWT authentication
- ✅ `requirements.txt` - Added PyJWT
- ✅ `.gitignore` - Ignore sensitive files
- ✅ `DEPLOYMENT.md` - Deployment guide
- ✅ `AUTHENTICATION.md` - Auth guide
- ✅ `README.md` - Project overview

---

## 🚦 You're Ready!

Everything is configured and ready to deploy. Choose your hosting platform and follow the steps in `DEPLOYMENT.md`.

**Recommendation**: Start with Vercel to test, but be prepared to switch to Railway if background tasks timeout.
