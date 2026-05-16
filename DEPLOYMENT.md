# 🚀 Deployment Guide - Vercel Frontend + Backend

This guide will help you deploy your BugFinderFixer application with the frontend on Vercel and backend on a hosting service.

## 📋 Overview

- **Frontend**: Deploy to Vercel (Free tier available)
- **Backend**: Deploy to Render, Railway, or PythonAnywhere (Free tiers available)
- **Configuration**: Environment variables for seamless connection

## 🎯 Part 1: Deploy Frontend to Vercel

### Step 1: Prepare Frontend

1. **Ensure package.json has build script** (already configured):
   ```json
   "scripts": {
     "build": "react-scripts build"
   }
   ```

2. **Create `.env.local` for local testing**:
   ```bash
   cd frontend
   cp .env.example .env.local
   ```

### Step 2: Deploy to Vercel

#### Option A: Vercel CLI (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend folder
cd frontend

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? bugfinderfixer (or your choice)
# - Directory? ./ (current directory)
# - Override settings? No

# For production deployment
vercel --prod
```

#### Option B: Vercel Dashboard

1. Go to [vercel.com](https://vercel.com)
2. Click **"Add New Project"**
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
5. Click **"Deploy"**

### Step 3: Configure Environment Variables on Vercel

1. Go to your project on Vercel
2. Click **Settings** → **Environment Variables**
3. Add:
   ```
   Name: REACT_APP_API_URL
   Value: https://your-backend-url.com
   ```
4. Click **"Save"**
5. **Redeploy** to apply changes

### Step 4: Note Your Vercel URL

Your frontend will be at: `https://your-app.vercel.app`

---

## 🖥️ Part 2: Deploy Backend

### Option A: Deploy to Render (Recommended - Free Tier)

#### Step 1: Prepare Backend

1. **Create `render.yaml`** in project root:
   ```yaml
   services:
     - type: web
       name: bugfinderfixer-api
       env: python
       buildCommand: pip install -r backend/requirements.txt
       startCommand: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
       envVars:
         - key: ALLOWED_ORIGINS
           value: https://your-app.vercel.app,http://localhost:3000
         - key: PYTHON_VERSION
           value: 3.11.0
   ```

#### Step 2: Deploy to Render

1. Go to [render.com](https://render.com)
2. Sign up/Login with GitHub
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository
5. Configure:
   - **Name**: bugfinderfixer-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add Environment Variables:
   ```
   ALLOWED_ORIGINS=https://your-app.vercel.app,http://localhost:3000
   ```
7. Click **"Create Web Service"**

#### Step 3: Get Backend URL

Your backend will be at: `https://bugfinderfixer-api.onrender.com`

---

### Option B: Deploy to Railway (Alternative)

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repository
5. Configure:
   - **Root Directory**: `backend`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add Environment Variables:
   ```
   ALLOWED_ORIGINS=https://your-app.vercel.app
   ```
7. Deploy

---

### Option C: Deploy to PythonAnywhere (Alternative)

1. Go to [pythonanywhere.com](https://pythonanywhere.com)
2. Sign up for free account
3. Upload your backend code
4. Configure WSGI file
5. Set environment variables
6. Start web app

---

## 🔗 Part 3: Connect Frontend to Backend

### Step 1: Update Vercel Environment Variable

1. Go to Vercel Dashboard → Your Project
2. Settings → Environment Variables
3. Update `REACT_APP_API_URL`:
   ```
   REACT_APP_API_URL=https://bugfinderfixer-api.onrender.com
   ```
4. Redeploy

### Step 2: Update Backend CORS

1. Go to Render Dashboard → Your Service
2. Environment → Add Variable:
   ```
   ALLOWED_ORIGINS=https://your-app.vercel.app,http://localhost:3000
   ```
3. Save and redeploy

### Step 3: Test Connection

1. Visit your Vercel URL: `https://your-app.vercel.app`
2. Try analyzing code
3. Check browser console for errors
4. Verify API calls are going to your backend

---

## ✅ Verification Checklist

### Frontend (Vercel)
- [ ] Site loads at Vercel URL
- [ ] No console errors
- [ ] UI displays correctly
- [ ] Sample code loads

### Backend (Render/Railway)
- [ ] API responds at `/health` endpoint
- [ ] Swagger docs accessible at `/docs`
- [ ] CORS allows Vercel domain

### Connection
- [ ] Frontend can call backend API
- [ ] Code analysis works
- [ ] No CORS errors in console
- [ ] Results display correctly

---

## 🐛 Troubleshooting

### CORS Error

**Problem**: `Access to fetch at 'https://backend.com' from origin 'https://frontend.vercel.app' has been blocked by CORS`

**Solution**:
1. Check backend `ALLOWED_ORIGINS` includes your Vercel URL
2. Ensure no trailing slashes in URLs
3. Redeploy backend after changing environment variables

### API Not Found (404)

**Problem**: Frontend shows "API endpoint not found"

**Solution**:
1. Verify `REACT_APP_API_URL` is set correctly on Vercel
2. Check backend is running (visit `/health` endpoint)
3. Ensure backend routes are correct (`/api/analyze`)

### Build Fails on Vercel

**Problem**: Build fails with module errors

**Solution**:
1. Check `package.json` dependencies
2. Ensure `build` script exists
3. Verify Node version compatibility
4. Check build logs for specific errors

### Backend Timeout

**Problem**: Requests timeout or take too long

**Solution**:
1. Free tier services may sleep after inactivity
2. First request might be slow (cold start)
3. Consider upgrading to paid tier for better performance

---

## 📊 Monitoring

### Vercel Analytics
- Go to your project → Analytics
- View page views, performance metrics

### Render Logs
- Go to your service → Logs
- Monitor API requests and errors

### Error Tracking (Optional)
Consider adding:
- **Sentry** for error tracking
- **LogRocket** for session replay
- **Google Analytics** for usage stats

---

## 🔄 Continuous Deployment

### Automatic Deployments

Both Vercel and Render support automatic deployments:

1. **Push to GitHub** → Automatic deployment
2. **Pull Request** → Preview deployment
3. **Merge to main** → Production deployment

### Manual Deployments

```bash
# Vercel
cd frontend
vercel --prod

# Render
# Push to GitHub or use Render Dashboard
```

---

## 💰 Cost Considerations

### Free Tiers

**Vercel (Frontend)**:
- ✅ Unlimited deployments
- ✅ 100GB bandwidth/month
- ✅ Custom domains
- ✅ Automatic HTTPS

**Render (Backend)**:
- ✅ 750 hours/month (enough for 1 service)
- ✅ Automatic HTTPS
- ⚠️ Sleeps after 15 min inactivity
- ⚠️ Cold starts (slow first request)

### Paid Upgrades

If you need better performance:
- **Vercel Pro**: $20/month (better bandwidth, analytics)
- **Render Starter**: $7/month (no sleep, faster)

---

## 🎉 Success!

Your BugFinderFixer is now live!

**Frontend**: `https://your-app.vercel.app`  
**Backend**: `https://bugfinderfixer-api.onrender.com`  
**API Docs**: `https://bugfinderfixer-api.onrender.com/docs`

Share your app with the world! 🚀

---

## 📝 Post-Deployment Tasks

1. **Update README.md** with live URLs
2. **Add badges** for deployment status
3. **Set up monitoring** and alerts
4. **Configure custom domain** (optional)
5. **Add analytics** tracking
6. **Set up error tracking**
7. **Create user documentation**

---

## 🔐 Security Best Practices

1. **Never commit `.env` files**
2. **Use environment variables** for all secrets
3. **Enable HTTPS** (automatic on Vercel/Render)
4. **Limit CORS** to specific domains
5. **Add rate limiting** (future enhancement)
6. **Monitor for suspicious activity**

---

## 📞 Support

- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev

---

Made with ❤️ by Bob