# ✅ Custom Domain Verification Guide

## How to Verify Your Custom Domain is Working

Since you've already added your custom domain, here's how to verify everything is set up correctly.

---

## 🔍 Verification Steps

### 1. Check Render Dashboard

1. Go to your Render service dashboard
2. Click **Settings** tab
3. Scroll to **Custom Domains** section
4. Check status:
   - ✅ **Verified** = DNS configured correctly
   - ⏳ **Pending** = Waiting for DNS propagation
   - ❌ **Failed** = DNS not configured correctly

### 2. Test Your Custom Domain

**Visit your custom domain:**
- `https://algobank.chaitanyahandore.com` (or your subdomain)

**What to check:**
- ✅ Page loads correctly
- ✅ Shows padlock icon (SSL working)
- ✅ URL shows `https://` (not `http://`)
- ✅ No SSL certificate warnings

### 3. Test HTTP Redirect

**Try visiting HTTP version:**
- `http://algobank.chaitanyahandore.com`
- Should automatically redirect to HTTPS
- Browser should show permanent redirect (301)

### 4. Check DNS Propagation

**Using Command Line:**
```bash
nslookup algobank.chaitanyahandore.com
dig algobank.chaitanyahandore.com
```

**Using Online Tools:**
- https://dnschecker.org
- https://www.whatsmydns.net

**What to look for:**
- CNAME record should point to `algobank.onrender.com`
- Or A record pointing to Render's IP (if using apex domain)

### 5. SSL Certificate Check

**Online SSL Checker:**
- Visit: https://www.ssllabs.com/ssltest/
- Enter your domain: `algobank.chaitanyahandore.com`
- Check certificate grade (should be A or A+)

**In Browser:**
- Click padlock icon in address bar
- Should show "Certificate is valid"
- Issued by Let's Encrypt (or Render's certificate authority)

---

## 🛠️ Troubleshooting

### Domain Not Resolving

**Symptoms:**
- Browser shows "This site can't be reached"
- DNS lookup fails

**Solutions:**
1. **Check DNS Records:**
   - Verify CNAME record is correct
   - Value should be: `algobank.onrender.com`
   - TTL: 3600 or Automatic

2. **Wait Longer:**
   - DNS can take up to 48 hours
   - Usually 5-30 minutes
   - Check propagation: https://dnschecker.org

3. **Clear DNS Cache:**
   ```bash
   # macOS
   sudo dscacheutil -flushcache
   
   # Windows
   ipconfig /flushdns
   
   # Linux
   sudo systemd-resolve --flush-caches
   ```

### SSL Certificate Not Working

**Symptoms:**
- Browser shows "Not Secure" warning
- SSL certificate error

**Solutions:**
1. **Wait for Provisioning:**
   - Render auto-provisions SSL
   - Usually takes 1-5 minutes after DNS verification
   - Check Render dashboard → Custom Domains

2. **Verify DNS is Correct:**
   - SSL can't be issued if DNS isn't verified
   - Ensure domain shows "Verified" in Render

3. **Check Certificate Status:**
   - Render Dashboard → Settings → Custom Domains
   - Should show "Certificate Active" or similar

### Domain Shows "Pending" in Render

**Solutions:**
1. **Double-check DNS Record:**
   - Ensure CNAME/A record is exactly as Render specified
   - Check for typos
   - Verify TTL is not 0

2. **Check Domain Registrar:**
   - Ensure DNS settings are saved
   - Some registrars need time to propagate

3. **Contact Support:**
   - If pending for more than 24 hours
   - Render support can help verify DNS

### Both HTTP and HTTPS Not Working

**Check:**
1. Is Render service running? (Check dashboard status)
2. Is DNS pointing to correct Render URL?
3. Are there any firewall rules blocking?

---

## ✅ Success Checklist

Your custom domain is working correctly if:

- [ ] Domain shows "Verified" in Render dashboard
- [ ] Website loads at `https://algobank.chaitanyahandore.com`
- [ ] HTTP redirects to HTTPS automatically
- [ ] Padlock icon shows in browser
- [ ] SSL certificate is valid (no warnings)
- [ ] All pages load correctly
- [ ] DNS checker shows correct CNAME/A record
- [ ] SSL Labs test shows A or A+ rating

---

## 🔒 Security Verification

### Check Security Headers:

Visit: https://securityheaders.com

Enter your custom domain and check:
- ✅ HTTPS enforced
- ✅ Security headers present
- ✅ HSTS enabled
- ✅ No mixed content warnings

---

## 📱 Mobile Testing

Test your custom domain on mobile:
- iOS Safari
- Android Chrome
- Should work the same as desktop

---

## 🔄 Updating Domain

If you need to change subdomain:

1. **Remove old domain in Render:**
   - Settings → Custom Domains
   - Delete old domain

2. **Add new DNS record:**
   - Use new subdomain name

3. **Add new domain in Render:**
   - Add new custom domain

---

## 📊 Current Status

**Your Setup:**
- **Custom Domain:** `algobank.chaitanyahandore.com` (or your subdomain)
- **Render URL:** `algobank.onrender.com`
- **SSL:** Auto-provisioned by Render
- **HTTPS Enforcement:** ✅ Enabled in code
- **Security Headers:** ✅ Implemented

---

## 🎯 Quick Test Commands

**Test DNS:**
```bash
nslookup algobank.chaitanyahandore.com
```

**Test HTTPS:**
```bash
curl -I https://algobank.chaitanyahandore.com
```

**Check SSL:**
```bash
openssl s_client -connect algobank.chaitanyahandore.com:443
```

---

## 📞 If You Need Help

1. **Check Render Logs:**
   - Dashboard → Logs tab
   - Look for any errors

2. **Render Documentation:**
   - https://render.com/docs/custom-domains

3. **Render Support:**
   - Dashboard → Support
   - They can help with DNS/SSL issues

---

**Your custom domain should be working!** 🎉

If you're experiencing any issues, check the troubleshooting section above or let me know what specific problem you're seeing.

