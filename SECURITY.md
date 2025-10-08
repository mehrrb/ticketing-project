# Security Configuration Guide

## 🔒 Environment Variables Setup

### 1. Create .env file
```bash
# Copy the example file
cp .env.example .env
```

### 2. Configure your .env file
```env
# Django Settings
SECRET_KEY=your-super-secret-key-here-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database Settings
POSTGRES_NAME=postgres
POSTGRES_USER=myuser
POSTGRES_PASSWORD=your-secure-password-here
POSTGRES_HOST=postgres_db
POSTGRES_PORT=5432

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME_DAYS=1
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
```

## 🛡️ Security Features Implemented

### ✅ Fixed Security Issues:
1. **SECRET_KEY**: Now loaded from environment variables
2. **DEBUG**: Controlled by environment variable
3. **ALLOWED_HOSTS**: Restricted to specific hosts
4. **Exception Handling**: Proper error handling without information leakage
5. **JWT Security**: Enhanced with token rotation and blacklisting
6. **HTTPS Security**: HSTS, XSS protection, content type sniffing protection

### 🔐 Additional Security Headers:
- `SECURE_BROWSER_XSS_FILTER = True`
- `SECURE_CONTENT_TYPE_NOSNIFF = True`
- `X_FRAME_OPTIONS = 'DENY'`
- `SECURE_HSTS_SECONDS = 31536000`
- `CSRF_COOKIE_SECURE = True`
- `SESSION_COOKIE_SECURE = True`

## 🚨 Important Security Notes:

1. **NEVER** commit `.env` file to version control
2. **ALWAYS** use strong, unique SECRET_KEY in production
3. **SET** DEBUG=False in production
4. **RESTRICT** ALLOWED_HOSTS to your actual domains
5. **USE** HTTPS in production
6. **ROTATE** JWT tokens regularly

## 🔧 Production Deployment:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SECRET_KEY="your-production-secret-key"
export DEBUG="False"
export ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Run server
python manage.py runserver
```

## 📋 Security Checklist:

- [ ] SECRET_KEY is set and secure
- [ ] DEBUG=False in production
- [ ] ALLOWED_HOSTS is restricted
- [ ] HTTPS is enabled
- [ ] Database credentials are secure
- [ ] JWT tokens have appropriate lifetime
- [ ] Error messages don't leak information
- [ ] Input validation is implemented
- [ ] Authentication is properly handled
