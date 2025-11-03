# 🏦 AlgoBank — Advanced DSA-Driven Banking Simulation

**AlgoBank** is a full-stack data-structures-and-algorithms project that simulates a digital banking ecosystem.  
It integrates real-world problems — transaction routing, fraud detection, ledger integrity, and interest accrual —  
solved using *advanced DSA techniques*.

---

## 🚀 Features & Algorithms

| Feature | DSA Concept | Description |
|----------|--------------|-------------|
| 💸 **ATM Optimizer** | Dynamic Programming | Determines minimum number of notes to dispense efficiently. |
| 🧾 **Ledger System** | Hash Maps | Real-time O(1) balance lookups and double-entry validation. |
| 🌲 **Transaction Integrity** | Merkle Tree | Cryptographic proof of transaction history authenticity. |
| 💰 **Interest Engine** | Segment Tree | Efficient range updates and point queries in O(log n). |
| 🕵️ **Fraud Detection** | Disjoint Set Union | Identifies connected clusters of suspicious accounts. |
| 🌐 **Routing System** | Dijkstra’s Algorithm | Computes least-cost path between banks using a priority queue. |

---

## 🧠 Tech Stack
- **Language:** Python 3.12  
- **Web Framework:** Flask 3.0
- **Frontend:** HTML5, CSS3, JavaScript
- **Testing:** Pytest  
- **Algorithms:** Graphs, DP, Trees, Union-Find, HashMaps  
- **Complexity:** O(E log V) (routing) | O(log n) (segment updates) | O(α(n)) (fraud union)

---

## 🧪 Run Locally

### Web Application (Recommended)
```bash
git clone https://github.com/ChaitanyaHandore/algobank.git
cd algobank/AlgoBank
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Then open your browser to **http://localhost:8080**

**Note:** If port 8080 is in use, the app will use the PORT environment variable. Port 5000 may conflict with macOS AirPlay Receiver.

**Demo Login:** Any username/password works in demo mode.

### Command Line Demo
```bash
python3 -m src.main   # run full simulation
```

### Run Tests
```bash
pytest -v       # run all tests
```

---

## 🌐 Web Application Features

- **🏠 Dashboard** - View account balance and quick actions
- **💸 Money Transfer** - Transfer funds between accounts
- **📊 Transaction History** - View all past transactions with downloadable statements
- **💳 Virtual Cards** - View card details with show/hide functionality
- **🏧 ATM Calculator** - Optimize note dispensation using DP
- **🌐 Bank Routing** - Find cheapest interbank routes using Dijkstra's
- **🕵️ Fraud Detection** - Detect connected suspicious accounts using DSU
- **💰 Investments** - Fixed Deposits, Recurring Deposits, Tax Saver Deposits
- **🏦 Loans** - Various loan types with interest rates and terms
- **⚙️ Services** - Mobile recharge, bill payment, add payees, and more
- **👤 Profile** - User account management and security settings

---

## 🚀 Deployment

**⚠️ Important:** GitHub Pages only supports static websites. Since AlgoBank is a Flask application (requires Python server), it **cannot be deployed directly on GitHub Pages**.

### Recommended Deployment Options:

#### 1. **Render** (Recommended - Free Tier Available)
1. Sign up at [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository: `https://github.com/ChaitanyaHandore/algobank`
4. Configure:
   - **Build Command:** `cd AlgoBank && pip install -r requirements.txt`
   - **Start Command:** `cd AlgoBank && python app.py`
   - **Environment:** Python 3
5. Click "Create Web Service"

#### 2. **Railway** (Easy & Free Tier)
1. Sign up at [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Flask and deploy

#### 3. **Heroku** (Requires Credit Card)
1. Install Heroku CLI
2. Procfile already included: `web: python app.py`
3. Deploy: `git push heroku main`

#### 4. **Vercel** (For Static + Serverless)
1. Install Vercel CLI: `npm i -g vercel`
2. Create `vercel.json`:
```json
{
  "builds": [{
    "src": "AlgoBank/app.py",
    "use": "@vercel/python"
  }]
}
```
3. Deploy: `vercel`

---

## 📝 Deployment Files

For quick deployment, you can use these files:

**For Render/Railway/Heroku:**
- `requirements.txt` - Already included
- `Procfile` - Already included: `web: python app.py`
- `runtime.txt` - Python 3.12.0 specification

**Environment Variables:**
- `PORT` - Automatically set by most platforms
- `FLASK_ENV` - Set to `production` for production deployments

---

## 🌐 Custom Domain Setup

All recommended platforms support custom domains with free SSL certificates. Here's how to set it up:

### Step 1: Purchase a Domain
- **Recommended providers:** Namecheap, GoDaddy, Google Domains, Cloudflare
- Domain examples: `algobank.com`, `algobank.io`, `myalgobank.com`

### Step 2: Configure DNS Records

#### For Render:
1. Go to your service dashboard → **Settings** → **Custom Domains**
2. Click **Add Custom Domain**
3. Enter your domain (e.g., `algobank.com` or `www.algobank.com`)
4. Render will provide DNS records to add:
   - **For apex domain** (`algobank.com`):
     - Type: `ALIAS` or `A` record
     - Name: `@` or leave blank
     - Value: Render's provided IP/URL
   - **For subdomain** (`www.algobank.com`):
     - Type: `CNAME`
     - Name: `www`
     - Value: Render's provided CNAME
5. Add these records in your domain registrar's DNS settings
6. Wait for DNS propagation (5-30 minutes)
7. Render automatically provisions SSL certificate (HTTPS)

#### For Railway:
1. Go to **Settings** → **Domains**
2. Click **Generate Domain**
3. Copy the provided DNS record
4. Add to your domain registrar:
   - Type: `CNAME`
   - Name: `@` (or `www` for subdomain)
   - Value: Railway's provided CNAME
5. Railway auto-configures SSL

#### For Heroku:
1. Install Heroku CLI: `heroku domains:add algobank.com`
2. Get DNS target: `heroku domains`
3. Add DNS records:
   - **For apex:** Add `ALIAS` or `A` record pointing to Heroku
   - **For subdomain:** Add `CNAME` record
4. Heroku provides SSL automatically

### Step 3: Flask Configuration (Already Updated)

The app is already configured for production deployment:
- Uses environment variables for `PORT` and `HOST`
- Automatically disables debug mode in production
- Listens on all interfaces (`0.0.0.0`) for deployment platforms

### Step 4: DNS Record Examples

**For Render (Apex Domain):**
```
Type: ALIAS or A
Name: @
Value: (provided by Render)
TTL: 3600
```

**For Subdomain:**
```
Type: CNAME
Name: www
Value: your-app.onrender.com
TTL: 3600
```

### Step 5: Verify Setup
1. Wait 5-30 minutes for DNS propagation
2. Check DNS: Use `nslookup algobank.com` or online tools like `whatsmydns.net`
3. Visit your custom domain: `https://algobank.com`
4. Verify SSL: Should show padlock icon in browser

### Common Issues:
- **DNS not resolving:** Wait longer (can take up to 48 hours, usually 5-30 min)
- **SSL not working:** Wait for automatic provisioning (usually 1-5 minutes after DNS)
- **Mixed content:** Ensure all URLs use HTTPS in your code

### Free Domain Options:
- **Freenom** (.tk, .ml, .ga, .cf domains - free but less reliable)
- **GitHub Student Pack** (includes free domain from Namecheap)
- **Subdomains:** Use free subdomains from services like `noip.com`