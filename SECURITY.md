# 🔒 AlgoBank Security Guide

## Security Best Practices for Production

This guide covers essential security measures for your AlgoBank Flask application.

---

## 🚨 Critical Security Measures

### 1. **Secret Key Management** ⚠️ CRITICAL

**Current Issue:** Using hardcoded secret key in `app.py`

**Fix:**
- Generate a secure random key
- Store in environment variables
- Never commit secrets to Git

**Implementation:**
```python
import os
import secrets

# Generate secure key (run once, then store in environment)
# secret_key = secrets.token_hex(32)
# print(secret_key)

# In app.py:
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
```

**For Render:**
- Go to Dashboard → Settings → Environment
- Add: `SECRET_KEY` = (generated secure key)

---

### 2. **Security Headers**

Add security headers to prevent common attacks:

**Implementation:**
```python
from flask import Flask
from functools import wraps

@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
    return response
```

---

### 3. **HTTPS/SSL** ✅ Enforced

**What's Implemented:**
- ✅ HTTP to HTTPS redirect (in code)
- ✅ Render automatically provides SSL certificates
- ✅ HTTPS is enforced automatically by Render
- ✅ Custom domains get SSL automatically
- ✅ HSTS (HTTP Strict Transport Security) header enabled
- ✅ Secure session cookies (only over HTTPS)

**How It Works:**
- Render automatically redirects HTTP → HTTPS at the platform level
- Code also enforces HTTPS redirect as a safety measure
- HSTS header tells browsers to always use HTTPS (1 year)
- Secure cookies ensure session data only sent over HTTPS

**Test:**
- Try visiting: `http://algobank.onrender.com` (should redirect to HTTPS)
- Check browser console for security warnings (should be none)

---

### 4. **Input Validation**

**Current:** Basic form validation
**Needed:** Comprehensive input sanitization

**Best Practices:**
- Validate all user inputs
- Sanitize data before processing
- Use Flask-WTF for form validation
- Prevent SQL injection (not applicable for in-memory storage)
- Prevent XSS attacks

---

### 5. **Session Security**

**Improvements:**
- Use secure cookies
- Set session timeout
- Regenerate session ID after login
- Use SameSite cookie attribute

---

### 6. **Rate Limiting**

Prevent abuse and brute force attacks:

**Install:**
```bash
pip install flask-limiter
```

**Implementation:**
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # Login logic
```

---

### 7. **Environment Variables**

**Never hardcode:**
- Secret keys
- API keys
- Database credentials
- Service URLs

**Always use:**
- Environment variables
- `.env` file for local (add to `.gitignore`)
- Platform environment variables for production

---

### 8. **Error Handling**

**Security Best Practices:**
- Don't expose internal errors to users
- Log errors securely
- Use generic error messages
- Hide stack traces in production

---

### 9. **CORS (If Needed)**

If you add API endpoints for external use:
```python
from flask_cors import CORS

# Only allow specific origins
CORS(app, origins=["https://yourdomain.com"])
```

---

### 10. **Dependency Updates**

Regularly update dependencies:
```bash
pip list --outdated
pip install --upgrade package-name
```

Check for vulnerabilities:
```bash
pip install safety
safety check
```

---

## 🛡️ Security Checklist

### Production Deployment:

- [ ] Change secret key to environment variable
- [ ] Add security headers middleware
- [ ] Implement rate limiting
- [ ] Set secure session cookies
- [ ] Validate all user inputs
- [ ] Enable HTTPS only (Render does this)
- [ ] Remove debug mode in production
- [ ] Set up error logging
- [ ] Review and update dependencies
- [ ] Configure CSP (Content Security Policy)
- [ ] Set up monitoring/alerts
- [ ] Regular security audits

---

## 🔧 Implementation Steps

### Step 1: Update Secret Key

1. Generate secure key:
```python
import secrets
print(secrets.token_hex(32))
```

2. Add to Render: Settings → Environment → `SECRET_KEY`

3. Update `app.py`:
```python
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-for-dev-only')
```

### Step 2: Add Security Headers

Add to `app.py` after creating app instance.

### Step 3: Implement Rate Limiting

Add flask-limiter for login and API endpoints.

### Step 4: Secure Sessions

Configure secure cookie settings.

---

## 📋 Security Headers Explained

| Header | Purpose |
|--------|---------|
| `X-Content-Type-Options: nosniff` | Prevents MIME type sniffing |
| `X-Frame-Options: DENY` | Prevents clickjacking |
| `X-XSS-Protection` | Enables XSS filter in older browsers |
| `Strict-Transport-Security` | Forces HTTPS |
| `Content-Security-Policy` | Controls resource loading |

---

## 🔍 Security Testing

### Tools to Use:

1. **OWASP ZAP** - Security scanner
2. **Burp Suite** - Web vulnerability scanner
3. **Nmap** - Network security scanner
4. **SSL Labs** - SSL/TLS testing

### Manual Checks:

- [ ] Test authentication bypass attempts
- [ ] Test SQL injection (if using database)
- [ ] Test XSS vulnerabilities
- [ ] Test CSRF protection
- [ ] Check for exposed sensitive data
- [ ] Verify HTTPS enforcement
- [ ] Test rate limiting

---

## 🚨 Common Vulnerabilities to Avoid

1. **Injection Attacks**
   - SQL Injection (not applicable - no database)
   - Command Injection
   - Template Injection

2. **Broken Authentication**
   - Weak passwords (currently demo mode)
   - Session hijacking
   - No rate limiting on login

3. **Sensitive Data Exposure**
   - Don't log passwords
   - Don't expose secrets in error messages
   - Encrypt sensitive data

4. **XML External Entities (XXE)**
   - Not applicable unless using XML

5. **Broken Access Control**
   - Validate user permissions
   - Check session validity

6. **Security Misconfiguration**
   - Default credentials
   - Debug mode enabled
   - Unnecessary features enabled

7. **XSS (Cross-Site Scripting)**
   - Sanitize user inputs
   - Use template escaping (Flask does this)

8. **Insecure Deserialization**
   - Be careful with JSON inputs
   - Validate all data

9. **Using Components with Known Vulnerabilities**
   - Keep dependencies updated
   - Use `safety` to check

10. **Insufficient Logging & Monitoring**
    - Log security events
    - Monitor for suspicious activity

---

## 📝 Render-Specific Security

### Environment Variables (Secure Storage):

1. Go to Render Dashboard
2. Settings → Environment
3. Add sensitive variables:
   - `SECRET_KEY`
   - Any API keys
   - Database credentials (if added later)

### SSL/TLS:
- ✅ Automatically configured
- ✅ Free SSL certificates
- ✅ HTTPS enforced

### Network Security:
- ✅ DDoS protection
- ✅ Firewall protection
- ✅ Secure infrastructure

---

## 🔐 Additional Recommendations

### For Production:

1. **Add Authentication:**
   - Implement proper user authentication
   - Use Flask-Login
   - Hash passwords (bcrypt)
   - Two-factor authentication

2. **Database Security:**
   - If adding database later:
     - Use parameterized queries
     - Encrypt sensitive columns
     - Regular backups
     - Access control

3. **API Security:**
   - Use API keys for external access
   - Implement JWT tokens
   - Rate limit API endpoints

4. **Monitoring:**
   - Set up error tracking (Sentry)
   - Monitor failed login attempts
   - Alert on suspicious activity

---

## 📚 Resources

- **OWASP Top 10:** https://owasp.org/www-project-top-ten/
- **Flask Security Best Practices:** https://flask.palletsprojects.com/en/latest/security/
- **Render Security:** https://render.com/docs/security
- **Mozilla Security Guidelines:** https://infosec.mozilla.org/guidelines/web_security

---

## 🎯 Quick Wins (Implement First)

1. ✅ Change secret key to environment variable
2. ✅ Add security headers
3. ✅ Implement rate limiting on login
4. ✅ Set secure session cookies
5. ✅ Remove debug mode in production

These provide the biggest security improvements with minimal effort!

