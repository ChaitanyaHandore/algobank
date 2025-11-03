# 🚀 Deploy AlgoBank on Render - Step by Step Guide

## Prerequisites
- GitHub account (your code is already at: https://github.com/ChaitanyaHandore/algobank)
- Render account (sign up at https://render.com - it's free!)

---

## Step-by-Step Deployment

### Step 1: Sign Up / Login to Render

1. Go to **https://render.com**
2. Click **Get Started for Free** (or **Sign In** if you have an account)
3. Sign up using:
   - **GitHub** (Recommended - one-click sign up)
   - Or Email/Password

---

### Step 2: Connect Your GitHub Repository

1. After signing in, you'll see the Render Dashboard
2. Click **New +** button (top right)
3. Select **Web Service**
4. Render will ask you to connect GitHub (if not connected):
   - Click **Connect GitHub** or **Configure account**
   - Authorize Render to access your repositories
   - Select the repositories you want to give access to (or all repos)

5. **Select Repository:**
   - Search for: `algobank` or `ChaitanyaHandore/algobank`
   - Click on your repository: `ChaitanyaHandore/algobank`

---

### Step 3: Configure Web Service

Fill in the following settings:

#### Basic Settings:

**Name:**
```
algobank
```
(Or any name you prefer)

**Region:**
```
Singapore (closest to you) or Frankfurt (EU)
```
(Choose closest to your location)

**Branch:**
```
main
```
(Should be selected by default)

**Root Directory:**
```
AlgoBank
```
⚠️ **IMPORTANT:** Since your Flask app is in the `AlgoBank` subdirectory, set this!

**Runtime:**
```
Python 3
```

#### Build & Deploy Settings:

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
python app.py
```

#### Advanced Settings (Click to expand):

**Environment Variables:**
Click **Add Environment Variable** and add:
- **Key:** `FLASK_ENV`
- **Value:** `production`

- **Key:** `PORT`
- **Value:** `8080`
(Note: Render sets PORT automatically, but this ensures compatibility)

**Plan:**
- Select **Free** (for testing)
- Or **Starter** ($7/month) for production with no sleep/spinning

---

### Step 4: Create Web Service

1. **Review all settings** above
2. Click **Create Web Service** button (bottom of page)

---

### Step 5: Wait for Deployment

1. Render will start building your application
2. You'll see build logs in real-time:
   - Installing dependencies from `requirements.txt`
   - Building your application
3. **First deployment takes 2-5 minutes**
4. Once complete, you'll see:
   - ✅ **Live** status
   - Your app URL: `https://algobank.onrender.com`

---

### Step 6: Test Your Deployment

1. Click on your app URL or open it in a new tab
2. You should see the AlgoBank login page
3. Test login with any username/password (demo mode)

**Your app is now live!** 🎉

---

## Adding Custom Domain (algobank.chaitanyahandore.com)

### Step 1: Go to Settings

1. In your Render service dashboard
2. Click **Settings** tab (left sidebar)

### Step 2: Add Custom Domain

1. Scroll down to **Custom Domains** section
2. Click **Add Custom Domain**
3. Enter your subdomain: `algobank.chaitanyahandore.com`
4. Click **Save**

### Step 3: Configure DNS

Render will show you DNS instructions:

**For Subdomain (algobank.chaitanyahandore.com):**
```
Type: CNAME
Name: algobank
Value: algobank.onrender.com
TTL: 3600
```

**Add this DNS record in your domain registrar:**
1. Go to your domain DNS settings (Namecheap/Cloudflare/etc.)
2. Add the CNAME record shown above
3. Wait 5-30 minutes for DNS propagation

### Step 4: SSL Certificate

- Render automatically provisions SSL certificate
- HTTPS will work automatically once DNS propagates
- Usually takes 1-5 minutes after DNS is verified

---

## Environment Variables Reference

You can set these in Render Dashboard → Settings → Environment:

| Variable | Value | Description |
|----------|-------|-------------|
| `FLASK_ENV` | `production` | Enables production mode |
| `FLASK_DEBUG` | `False` | Disables debug mode |
| `PORT` | `8080` | Port (usually auto-set by Render) |
| `HOST` | `0.0.0.0` | Host (auto-set by Render) |

---

## Deployment Checklist

- [ ] Signed up on Render
- [ ] Connected GitHub account
- [ ] Selected `ChaitanyaHandore/algobank` repository
- [ ] Set **Root Directory:** `AlgoBank` ⚠️ Important!
- [ ] Set **Build Command:** `pip install -r requirements.txt`
- [ ] Set **Start Command:** `python app.py`
- [ ] Added `FLASK_ENV=production` environment variable
- [ ] Clicked **Create Web Service**
- [ ] Waited for deployment to complete
- [ ] Tested the live URL
- [ ] Added custom domain (optional)
- [ ] Configured DNS records (if using custom domain)

---

## Common Issues & Solutions

### ❌ Build Fails: "No module named 'flask'"

**Solution:** 
- Check that `requirements.txt` exists in `AlgoBank` directory
- Verify Root Directory is set to `AlgoBank`

### ❌ App Crashes on Start

**Solution:**
- Check build logs for errors
- Verify `app.py` is in the `AlgoBank` directory
- Check that all imports are correct

### ❌ Port Already in Use

**Solution:**
- Render sets PORT automatically
- Remove any hardcoded port in `app.py` (already fixed in your code)

### ❌ 404 Errors

**Solution:**
- Ensure Root Directory is set to `AlgoBank`
- Check that all files are committed to GitHub
- Verify the build completed successfully

### ❌ Custom Domain Not Working

**Solution:**
- Wait longer for DNS propagation (up to 48 hours, usually 5-30 min)
- Verify DNS record is correct
- Check DNS propagation: https://dnschecker.org
- Ensure Render shows domain as "Verified"

---

## Free vs Paid Plans

### Free Plan:
- ✅ $0/month
- ✅ 750 hours/month (enough for testing)
- ⚠️ App spins down after 15 minutes of inactivity
- ⚠️ First request after spin-down takes ~30 seconds (cold start)
- ✅ SSL included
- ✅ Custom domains supported

### Starter Plan ($7/month):
- ✅ No spinning down
- ✅ Always available
- ✅ Better performance
- ✅ SSL included
- ✅ Custom domains supported

**Recommendation:** Start with Free plan, upgrade if needed.

---

## Automatic Deploys

Render automatically deploys when you push to GitHub:

1. **Default:** Auto-deploys on every push to `main` branch
2. **Manual Deploy:** You can disable auto-deploy and deploy manually
3. **Deploy Settings:** Configure in Settings → Auto-Deploy

**Settings:**
- **Auto-Deploy:** On (default)
- **Branch:** `main`
- **Pull Request Previews:** On/Off (your choice)

---

## Viewing Logs

1. Go to your service dashboard
2. Click **Logs** tab
3. See real-time application logs
4. Useful for debugging issues

---

## Managing Your Service

### Restart Service:
- Settings → Manual Deploy → Clear build cache & deploy

### Update Service:
- Just push to GitHub - Render auto-deploys

### Delete Service:
- Settings → Danger Zone → Delete Service

---

## Cost Summary

| Plan | Monthly Cost | Features |
|------|--------------|----------|
| **Free** | $0 | 750 hours, spins down after inactivity |
| **Starter** | $7 | Always on, better performance |

**Your Setup:**
- Hosting: Free (or $7/month if you upgrade)
- Domain: Already have `chaitanyahandore.com`
- Subdomain: Free (uses existing domain)
- SSL: Free (auto-provided by Render)

**Total: $0** (with free plan + existing domain)

---

## Next Steps After Deployment

1. ✅ Test all features on the live site
2. ✅ Add custom domain: `algobank.chaitanyahandore.com`
3. ✅ Configure DNS records
4. ✅ Share your live URL
5. ✅ Monitor logs for any issues

---

## Quick Reference

**Render Dashboard:** https://dashboard.render.com
**Your Repository:** https://github.com/ChaitanyaHandore/algobank
**Root Directory:** `AlgoBank` ⚠️ Important!
**Build Command:** `pip install -r requirements.txt`
**Start Command:** `python app.py`

---

## Support

- **Render Docs:** https://render.com/docs
- **Render Support:** https://render.com/docs/support
- **AlgoBank Issues:** Check GitHub repository

---

Good luck with your deployment! 🚀

