# Vercel Deployment Checklist for ReadWise Backend

## ✅ Pre-Deployment Steps Completed

1. **CORS Configuration** ✅
   - Added CORS middleware to allow frontend requests
   - Currently set to allow all origins (`*`) - update with your frontend URL after deployment

2. **Vercel Configuration** ✅
   - Created `vercel.json` for Vercel settings
   - Created `index.py` as entry point

3. **Dependencies** ✅
   - All dependencies listed in `requirements.txt`

4. **Authentication** ✅
   - JWT authentication implemented
   - Ready for Supabase integration

---

## 🚀 Deployment Steps

### 1. Push Code to GitHub

```bash
cd /home/hushrama/Desktop/Fastapi\ Projs/read-wise/backend
git init  # if not already a git repo
git add .
git commit -m "Prepare backend for Vercel deployment"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. Deploy to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click **"Add New Project"**
3. Import your GitHub repository
4. Vercel should auto-detect it as a Python project
5. Click **"Deploy"**

### 3. Configure Environment Variables in Vercel

After deployment, add these environment variables in **Vercel Dashboard** → **Settings** → **Environment Variables**:

#### Required Environment Variables:

```
DATABASE_URL=<your-supabase-postgres-connection-string>
SUPABASE_JWT_SECRET=WG2aDlX5D8wdkdxCFTWQRNhsJk3jCns4Kl8I/l/WtdfIX1b8ZhNqOAYf/EBfWSd+j5FbXforL0dij18/xXmU7w==
OPENAI_API_KEY=<your-openai-api-key>
```

**Important Notes:**
- Do NOT include quotes around the values
- Make sure to use the **pooling connection string** from Supabase for serverless environments
- Get it from: Supabase Dashboard → Settings → Database → Connection string → "Connection Pooling"

### 4. Update CORS After Deployment

Once you have your frontend URL, update CORS in `main.py`:

```python
allow_origins=["https://your-frontend-url.vercel.app"],
```

Then redeploy.

---

## 🔍 Post-Deployment Verification

Test your deployed API:

```bash
# Replace with your actual Vercel URL
curl https://your-backend.vercel.app/health
```

Expected response:
```json
{"status": "ok"}
```

---

## ⚠️ Important Notes for Vercel Hobby Plan

### 1. **Serverless Functions Timeout**
   - Vercel Hobby plan has a **10-second timeout** for serverless functions
   - Your AI processing might take longer than 10 seconds
   - **Solution**: Background tasks won't work properly on Vercel serverless
   
   **Recommendation**: Consider one of these options:
   - Use Vercel's paid plan (Pro) which has 60-second timeout
   - Use a different hosting platform (Railway, Render, or Fly.io) which support long-running processes
   - Modify the code to use a queue service (like Supabase Edge Functions or a webhook)

### 2. **Database Connection Pooling**
   - Use Supabase's **connection pooling** string (port 6543, not 5432)
   - Example: `postgresql://user:pass@host:6543/database?pgbouncer=true`
   - Our code already handles removing `pgbouncer=true` parameter

### 3. **No Persistent Storage**
   - Vercel serverless functions don't have persistent file storage
   - All uploads/PDFs are stored in memory temporarily
   - This is fine for your current implementation

### 4. **Cold Starts**
   - First request might be slow (2-5 seconds)
   - Subsequent requests will be faster

---

## 🎯 Recommended Alternative: Railway

If you encounter timeout issues with Vercel, I recommend **Railway** instead:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize and deploy
railway init
railway up
```

Railway advantages:
- No 10-second timeout
- Better for long-running AI tasks
- Still free tier available
- Supports background tasks

---

## 📝 Next Steps After Deployment

1. ✅ Get your deployed backend URL (e.g., `https://your-backend.vercel.app`)
2. ✅ Test the `/health` endpoint
3. ✅ Update CORS with your frontend URL
4. ✅ Move to frontend development
5. ✅ Configure frontend to use your deployed backend URL

---

## 🐛 Troubleshooting

### "500 Internal Server Error"
- Check Vercel logs (Dashboard → Deployment → Function Logs)
- Verify all environment variables are set correctly

### "Database connection failed"
- Ensure you're using the **pooling** connection string (port 6543)
- Check DATABASE_URL has the correct format

### "Token verification failed"
- Verify SUPABASE_JWT_SECRET is set correctly in Vercel
- Make sure there are no extra spaces or quotes

### "Function timeout"
- Background tasks might be timing out
- Consider splitting long operations or using a queue service
