# Deployment Guide

## Problem
Vercel serverless functions have a 250 MB limit, but our Python dependencies (pandas, numpy, scipy, statsmodels, etc.) exceed this limit.

## Solution: Split Deployment

### Frontend (Vercel) ✅
- The `web/` folder is already configured for Vercel
- Static files work fine on Vercel

### Backend API (Railway/Render/Fly.io)
Deploy the API separately on a platform that supports larger Python apps:

1. **Railway** (Recommended)
   - Connect your GitHub repo
   - Set `api_server.py` as the entry point
   - Add `OPENAI_API_KEY` environment variable
   - Railway will automatically detect Python and install from `requirements.txt`

2. **Render**
   - Create a new Web Service
   - Connect GitHub repo
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn api_server:app --host 0.0.0.0 --port $PORT`

3. **Update Frontend**
   - After deploying the API, update `web/app.js` to point to your API URL:
   ```javascript
   const API_URL = 'https://your-api.railway.app'; // or render.com, etc.
   const resp = await fetch(`${API_URL}/sector-analysis`, {
   ```

## Alternative: Full Stack on Railway
- Deploy both frontend and backend on Railway
- More control, but loses Vercel's CDN benefits

