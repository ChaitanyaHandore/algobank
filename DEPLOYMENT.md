# 🚀 AlgoBank Deployment Guide

## Custom Domain Setup Guide

### Quick Start for Custom Domain

1. **Deploy on Render/Railway/Heroku** (follow README deployment section)
2. **Purchase a domain** from Namecheap, GoDaddy, or Cloudflare
3. **Configure DNS** in your domain registrar
4. **Add domain** in your deployment platform
5. **SSL is automatic** - most platforms provide free SSL certificates

---

## Platform-Specific Custom Domain Instructions

### 🌟 Render.com

#### Step-by-Step:

1. **After deploying on Render:**
   - Go to your Web Service dashboard
   - Click on **Settings** tab
   - Scroll to **Custom Domains** section

2. **Add Custom Domain:**
   - Click **Add Custom Domain**
   - Enter your domain: `algobank.com` (or `www.algobank.com`)
   - Render will show you DNS records to add

3. **Configure DNS at Domain Registrar:**
   
   **For Apex Domain (algobank.com):**
   ```
   Type: ALIAS or A Record
   Name: @
   Value: (IP address provided by Render)
   TTL: 3600
   ```
   
   **For Subdomain (www.algobank.com):**
   ```
   Type: CNAME
   Name: www
   Value: your-app-name.onrender.com
   TTL: 3600
   ```

4. **Wait for DNS Propagation:**
   - Usually takes 5-30 minutes
   - Check status at: https://dnschecker.org

5. **SSL Certificate:**
   - Render automatically provisions SSL certificate
   - HTTPS will work automatically once DNS propagates

---

### 🚂 Railway.app

#### Step-by-Step:

1. **After deploying on Railway:**
   - Go to your project dashboard
   - Click on your service
   - Go to **Settings** tab → **Domains**

2. **Add Custom Domain:**
   - Click **Generate Domain** or **Add Domain**
   - Enter your domain name
   - Railway will provide DNS target

3. **Configure DNS:**
   ```
   Type: CNAME
   Name: @ (for apex) or www (for subdomain)
   Value: (provided by Railway)
   TTL: 3600
   ```

4. **Railway handles SSL automatically** via Let's Encrypt

---

### 🔷 Heroku

#### Step-by-Step:

1. **Install Heroku CLI** (if not installed):
   ```bash
   brew install heroku/brew/heroku  # macOS
   # or visit: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku:**
   ```bash
   heroku login
   ```

3. **Add Custom Domain:**
   ```bash
   heroku domains:add algobank.com
   heroku domains:add www.algobank.com  # Optional: for www subdomain
   ```

4. **Get DNS Target:**
   ```bash
   heroku domains
   ```
   This will show you the DNS target to configure

5. **Configure DNS at Domain Registrar:**
   - **For Apex:** Use `ALIAS` or `A` record pointing to Heroku's IP
   - **For Subdomain:** Use `CNAME` record

6. **SSL Certificate:**
   ```bash
   heroku certs:auto:enable
   ```
   Heroku provides automatic SSL via Let's Encrypt

---

## DNS Configuration Examples

### Namecheap DNS Settings:

1. Go to **Domain List** → Click **Manage**
2. Go to **Advanced DNS** tab
3. Add records:

**For Render (Apex):**
- Type: `ALIAS` Record
- Host: `@`
- Value: `your-app.onrender.com`
- TTL: Automatic

**For Subdomain:**
- Type: `CNAME` Record
- Host: `www`
- Value: `your-app.onrender.com`
- TTL: Automatic

### Cloudflare DNS Settings:

1. Select your domain in Cloudflare dashboard
2. Go to **DNS** section
3. Click **Add record**

**For Render:**
- Type: `CNAME`
- Name: `@` (for apex) or `www` (for subdomain)
- Target: `your-app.onrender.com`
- Proxy status: DNS only (gray cloud) or Proxied (orange cloud)
- TTL: Auto

**Note:** Cloudflare's proxy can cause issues with some platforms. If you have problems, disable proxy (gray cloud).

---

## Environment Variables for Production

Set these in your deployment platform:

```
PORT=8080 (auto-set by most platforms)
FLASK_ENV=production
FLASK_DEBUG=False
HOST=0.0.0.0 (auto-set by platforms)
```

---

## Verifying Your Setup

### 1. Check DNS Propagation:
```bash
# Using command line
nslookup algobank.com
dig algobank.com

# Or use online tools:
# - https://dnschecker.org
# - https://www.whatsmydns.net
```

### 2. Test HTTPS:
- Visit: `https://algobank.com`
- Check for padlock icon in browser
- Ensure no mixed content warnings

### 3. Test HTTP Redirect:
- Most platforms auto-redirect HTTP → HTTPS
- Visit: `http://algobank.com` (should redirect)

---

## Troubleshooting

### DNS Not Resolving:
- **Wait longer:** Can take up to 48 hours (usually 5-30 minutes)
- **Check TTL:** Lower TTL = faster updates
- **Clear DNS cache:**
  ```bash
  # macOS
  sudo dscacheutil -flushcache
  
  # Windows
  ipconfig /flushdns
  
  # Linux
  sudo systemd-resolve --flush-caches
  ```

### SSL Certificate Issues:
- **Wait for provisioning:** Usually 1-5 minutes after DNS
- **Check certificate status:** In platform dashboard
- **Renew manually** if needed (usually auto-renewed)

### Mixed Content Warnings:
- Ensure all resources use HTTPS
- Update any hardcoded `http://` URLs to `https://`
- Check browser console for mixed content errors

### Domain Not Loading:
- Verify DNS records are correct
- Check domain registrar's DNS settings
- Verify platform shows domain as active
- Check platform logs for errors

---

## Free Domain Options

### Option 1: Freenom (Free Domains)
- **TLDs:** .tk, .ml, .ga, .cf (free)
- **URL:** https://www.freenom.com
- **Note:** Less reliable, not recommended for production

### Option 2: GitHub Student Pack
- **Includes:** Free .me domain from Namecheap
- **URL:** https://education.github.com/pack
- **Requires:** Student email verification

### Option 3: Free Subdomain Services
- **No-IP:** https://www.noip.com (free subdomains)
- **DuckDNS:** https://www.duckdns.org (free subdomains)
- **Note:** Some platforms may not allow custom DNS for subdomains

---

## Cost Estimate

| Item | Cost | Notes |
|------|------|-------|
| Domain (.com) | $10-15/year | Namecheap, GoDaddy |
| Domain (.io) | $30-40/year | More expensive |
| SSL Certificate | FREE | Auto-provided by platforms |
| Hosting (Render Free) | FREE | With limitations |
| Hosting (Render Paid) | $7/month | No limitations |
| **Total (Free tier)** | **$10-15/year** | Domain only |

---

## Next Steps After Custom Domain Setup

1. ✅ **Update social media links** with your custom domain
2. ✅ **Update README** with live URL
3. ✅ **Set up email** (optional) - services like Mailgun for transactional emails
4. ✅ **Set up monitoring** - UptimeRobot for uptime monitoring (free)
5. ✅ **Enable analytics** - Google Analytics or Plausible
6. ✅ **Configure backups** - Most platforms have automatic backups

---

## Support

For issues specific to:
- **Render:** https://render.com/docs
- **Railway:** https://docs.railway.app
- **Heroku:** https://devcenter.heroku.com

For AlgoBank-specific issues, check the main README or open an issue on GitHub.

