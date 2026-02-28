# Django Backend Deployment Guide - PC Maintenance Management System

## Overview
This document provides comprehensive instructions for deploying the Django backend to production using Render.com or similar platforms.

## ✅ Pre-Deployment Checklist

### Completed Fixes
- [x] Fixed `wsgi.py` module references (was using `zenjitaste` instead of `backend`)
- [x] Created proper `deployment_settings.py` in `backend/` directory
- [x] Added `dj-database-url` to `requirements.txt` for PostgreSQL support
- [x] Fixed security issues:
  - [x] Changed `ALLOWED_HOSTS` from `['*']` to environment-based configuration
  - [x] Changed `CORS_ALLOW_ALL_ORIGINS` to restricted `CORS_ALLOWED_ORIGINS`
  - [x] Added `CSRF_TRUSTED_ORIGINS` for security
- [x] Created `.env.example` for environment variable documentation
- [x] Created `runtime.txt` for Python version specification
- [x] Added migration `__init__.py` files for all apps
- [x] Improved `build.sh` script with better error handling

### Environment Setup
Before deployment, you must configure these environment variables:

```env
# REQUIRED
SECRET_KEY=<generate-a-strong-secret-key>
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/dbname
RENDER_EXTERNAL_HOSTNAME=your-app.onrender.com

# SECURITY
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-app.onrender.com
CORS_ALLOWED_ORIGINS=https://your-frontend.onrender.com,https://yourdomain.com
CSRF_TRUSTED_ORIGINS=https://your-frontend.onrender.com,https://yourdomain.com

# OPTIONAL (if using email)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# OPTIONAL (for superuser creation)
CREATE_SUPERUSER=True
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@yourdomain.com
DJANGO_SUPERUSER_PASSWORD=<strong-password>
```

## 🚀 Deployment Steps

### Step 1: Generate Secret Key
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
Copy the output and set it in your deployment platform's environment variables.

### Step 2: Set Up Database (PostgreSQL on Render)
1. Create a PostgreSQL instance on Render.com
2. Copy the database connection string
3. Set `DATABASE_URL` in environment variables

### Step 3: Deploy to Render.com

#### Option A: Using build.sh (Recommended)
1. Create new Web Service on Render.com
2. Connect your Git repository
3. Set environment variables (see Environment Setup section)
4. Build command: `./build.sh`
5. Start command: `gunicorn backend.wsgi`

#### Option B: Manual Build Command
```bash
pip install -r requirements.txt && \
python manage.py collectstatic --noinput && \
python manage.py migrate
```

### Step 4: Verify Deployment
1. Check that static files are being served correctly
2. Test API endpoints:
   ```
   GET /api/auth/user/ (requires authentication)
   GET /api/services/ (public)
   GET /api/bookings/ (requires authentication)
   ```
3. Verify admin panel: `/admin/`

## 📋 Configuration Details

### Settings Structure
- **Development**: Uses `backend/settings.py` with SQLite
- **Production**: Uses `backend/deployment_settings.py` with PostgreSQL
- **WSGI Selection**: Automatically selects deployment settings if `RENDER_EXTERNAL_HOSTNAME` is set

### Database
- **Development**: SQLite (`db.sqlite3`)
- **Production**: PostgreSQL (via `DATABASE_URL`)
- **Connection Pooling**: Enabled for production (`conn_max_age=600`)
- **SSL**: Required for Render PostgreSQL (`ssl_require=True`)

### Static Files
- **Storage**: WhiteNoise with compressed manifest storage
- **Root Directory**: `staticfiles/`
- **Collection**: Automatic via build script

### Security Features
- **HTTPS Redirect**: Enabled in production
- **HSTS**: Configured with 1-year max-age
- **CSRF Protection**: Token validation with trusted origins
- **Session Cookies**: Secure flag set in production
- **Cross-Origin**: Restricted to specified origins

### Email Configuration
- **Backend**: SMTP (Gmail recommended for testing)
- **TLS**: Enabled
- **Port**: 587 (standard TLS)

## 🔍 Troubleshooting

### Database Connection Errors
```
Error: could not translate host name "postgres" to address
```
**Solution**: Ensure `DATABASE_URL` is correctly set with valid PostgreSQL credentials

### Static Files Not Loading
```
404 Not Found: /static/admin/css/base.css
```
**Solution**: 
1. Run `python manage.py collectstatic --noinput`
2. Verify `STATIC_ROOT` directory exists
3. Check WhiteNoise middleware is enabled

### Secret Key Error
```
ValueError: SECRET_KEY environment variable is required for production
```
**Solution**: Set `SECRET_KEY` in environment variables (see Step 1)

### CORS Errors
```
Error: Request blocked by CORS policy
```
**Solution**: 
1. Add your frontend URL to `CORS_ALLOWED_ORIGINS`
2. Add your frontend URL to `CSRF_TRUSTED_ORIGINS`
3. Ensure frontend matches exactly (protocol, domain, port)

### Migration Errors
```
Error: conflicting migrations detected
```
**Solution**:
1. Check migration files are in correct format
2. Ensure `__init__.py` exists in migration folders
3. Run: `python manage.py showmigrations` to see status

## 🔐 Security Reminders

1. **Never commit `.env` file** - Use environment variables only
2. **Never use DEBUG=True in production** - Set `DEBUG=False`
3. **Change default ALLOWED_HOSTS** - Set to your actual domain
4. **Use strong SECRET_KEY** - Generate with Django's security tools
5. **Enable HTTPS** - Always use HTTPS in production
6. **Restrict CORS** - Never use `CORS_ALLOW_ALL_ORIGINS=True`
7. **Secure Database** - Use complex password, restrict network access
8. **Monitor Logs** - Check deployment logs for warnings and errors

## 📞 Support & Debugging

### View Deployment Logs
**Render.com**: Dashboard > Service > Logs tab

### Common Log Messages
```
Starting gunicorn 21.2.0
Django version 4.2.9
Running collectstatic
Applying accounts.0001_initial... OK
Applying bookings.0001_initial... OK
Applying services.0001_initial... OK
```

### Local Testing Before Deployment
```bash
# Test with deployment settings locally
DJANGO_SETTINGS_MODULE=backend.deployment_settings python manage.py runserver

# Or set environment variable
export RENDER_EXTERNAL_HOSTNAME=localhost
python manage.py runserver
```

## 📝 API Endpoints Reference

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `POST /api/auth/logout/` - Logout user
- `GET /api/auth/user/` - Get current user (requires auth)
- `PUT /api/auth/profile/` - Update profile (requires auth)
- `POST /api/auth/change-password/` - Change password (requires auth)

### Services
- `GET /api/services/` - List all services
- `GET /api/services/{id}/` - Get service details
- `POST /api/services/` - Create service (admin only)
- `PUT /api/services/{id}/` - Update service (admin only)
- `DELETE /api/services/{id}/` - Delete service (admin only)
- `GET /api/services/stats/` - Service statistics (admin only)

### Bookings
- `GET /api/bookings/` - List user bookings (authenticated)
- `GET /api/bookings/{id}/` - Get booking details (authenticated)
- `POST /api/bookings/` - Create booking (authenticated)
- `PUT /api/bookings/{id}/` - Update booking (own or admin)
- `DELETE /api/bookings/{id}/` - Delete booking (own or admin)
- `POST /api/bookings/{id}/cancel/` - Cancel booking

## ✨ Next Steps

1. ✅ Test all endpoints locally before deployment
2. ✅ Set up error monitoring (Sentry recommended)
3. ✅ Configure email service if needed
4. ✅ Set up database backups
5. ✅ Monitor logs after deployment
6. ✅ Test with actual frontend application

---

**Last Updated**: February 28, 2026
**Django Version**: 4.2.9
**Python Version**: 3.11.7
