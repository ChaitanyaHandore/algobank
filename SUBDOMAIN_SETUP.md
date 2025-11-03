# 🌐 Setting Up AlgoBank on Subdomain (chaitanyahandore.com)

## Quick Setup for algobank.chaitanyahandore.com

Since you already have `chaitanyahandore.com` with your portfolio, we'll add AlgoBank as a subdomain.

---

## Step-by-Step Instructions

### Step 1: Deploy AlgoBank on Render/Railway

1. Deploy AlgoBank following the main README deployment instructions
2. Once deployed, you'll get a URL like: `your-app.onrender.com`

### Step 2: Configure Subdomain DNS

#### If your domain is on Namecheap:

1. **Go to Namecheap Dashboard**
   - Login to Namecheap
   - Go to **Domain List**
   - Click **Manage** next to `chaitanyahandore.com`

2. **Access DNS Settings**
   - Go to **Advanced DNS** tab

3. **Add CNAME Record for Subdomain**
   - Click **Add New Record**
   - Select **CNAME Record**
   - Configure:
     ```
     Type: CNAME Record
     Host: algobank
     Value: your-app-name.onrender.com
     TTL: Automatic (or 3600)
     ```
   - Click **Save**

4. **Save Changes**
   - The DNS changes will propagate in 5-30 minutes

#### If your domain is on Cloudflare:

1. **Go to Cloudflare Dashboard**
   - Select `chaitanyahandore.com`
   - Go to **DNS** section

2. **Add CNAME Record**
   - Click **Add record**
   - Configure:
     ```
     Type: CNAME
     Name: algobank
     Target: your-app-name.onrender.com
     Proxy status: DNS only (gray cloud) or Proxied (orange cloud)
     TTL: Auto
     ```
   - Click **Save**

**Note:** If you have issues with Cloudflare proxy, disable it (use gray cloud)

#### If your domain is on GoDaddy:

1. **Go to GoDaddy Dashboard**
   - My Products → **DNS** → `chaitanyahandore.com`

2. **Add CNAME Record**
   - Click **Add** → **CNAME**
   - Configure:
     ```
     Name: algobank
     Value: your-app-name.onrender.com
     TTL: 1 hour
     ```
   - Click **Save**

---

### Step 3: Configure Subdomain in Render

1. **Go to Render Dashboard**
   - Open your AlgoBank service
   - Go to **Settings** tab
   - Scroll to **Custom Domains**

2. **Add Custom Domain**
   - Click **Add Custom Domain**
   - Enter: `algobank.chaitanyahandore.com`
   - Click **Save**

3. **Wait for DNS Verification**
   - Render will verify the DNS record
   - This may take a few minutes

4. **SSL Certificate**
   - Render automatically provisions SSL
   - HTTPS will work automatically once verified

---

### Step 4: Alternative Subdomain Options

You can use any subdomain prefix:

- `algobank.chaitanyahandore.com` ✅
- `bank.chaitanyahandore.com` ✅
- `app.chaitanyahandore.com` ✅
- `demo.chaitanyahandore.com` ✅
- `banking.chaitanyahandore.com` ✅

Just replace `algobank` with your preferred prefix in the DNS CNAME record.

---

## DNS Configuration Summary

### CNAME Record Configuration:

```
Type: CNAME
Name: algobank
Value: your-app-name.onrender.com
TTL: 3600 (or Automatic)
```

This creates: `algobank.chaitanyahandore.com` → points to your Render app

---

## Verification Steps

### 1. Check DNS Propagation (5-30 minutes after setup):

```bash
# Using command line
nslookup algobank.chaitanyahandore.com
dig algobank.chaitanyahandore.com

# Or online tools:
# - https://dnschecker.org
# - https://www.whatsmydns.net
```

### 2. Test Your Subdomain:

- Visit: `https://algobank.chaitanyahandore.com`
- Should show your AlgoBank application
- Check for padlock icon (SSL working)

### 3. Verify Both Sites Work:

- Portfolio: `https://chaitanyahandore.com` ✅
- AlgoBank: `https://algobank.chaitanyahandore.com` ✅

---

## Troubleshooting

### Subdomain Not Resolving:

1. **Wait longer:** DNS can take up to 48 hours (usually 5-30 minutes)
2. **Check DNS record:** Ensure CNAME is exactly `your-app-name.onrender.com`
3. **Clear DNS cache:**
   ```bash
   # macOS
   sudo dscacheutil -flushcache
   
   # Windows
   ipconfig /flushdns
   ```
4. **Verify in Render:** Check that Render shows domain as verified

### SSL Not Working:

- Wait 1-5 minutes after DNS verification
- Render automatically provisions SSL via Let's Encrypt
- Check Render dashboard → Settings → Custom Domains for status

### Portfolio Site Affected:

- Adding a subdomain **does NOT affect** your main domain
- `chaitanyahandore.com` continues to work normally
- Only `algobank.chaitanyahandore.com` points to AlgoBank

---

## Multiple Subdomains Example

You can have multiple projects on subdomains:

```
chaitanyahandore.com          → Portfolio
algobank.chaitanyahandore.com → AlgoBank
blog.chaitanyahandore.com     → Blog
app.chaitanyahandore.com      → Another app
```

Each requires a separate CNAME record with different Host values.

---

## Cost

**Free!** 🎉

- No additional domain cost (using existing domain)
- Subdomains are free
- SSL certificate: Free (auto-provided by Render)
- Hosting: Free (Render free tier)

**Total Cost: $0** (assuming you're using free hosting tier)

---

## Next Steps

1. ✅ Deploy AlgoBank on Render
2. ✅ Add CNAME record for `algobank` subdomain
3. ✅ Configure subdomain in Render dashboard
4. ✅ Wait for DNS/SSL propagation
5. ✅ Visit `https://algobank.chaitanyahandore.com`

---

## Quick Reference

**DNS Record:**
- Type: `CNAME`
- Name: `algobank`
- Value: `your-render-app.onrender.com`

**Result:**
- Portfolio: `https://chaitanyahandore.com`
- AlgoBank: `https://algobank.chaitanyahandore.com`

Both sites will work independently on your domain! 🚀

