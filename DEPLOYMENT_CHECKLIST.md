# 🚀 Django Deployment Checklist - PC Maintenance Backend

## Pre-Deployment Setup
- [ ] Review all changes in `DEPLOYMENT_SUMMARY.md`
- [ ] Read the full deployment guide in `DEPLOYMENT.md`
- [ ] Remove old `accounts/deployment_settings.py` (if still exists)
- [ ] Test locally with: `python manage.py runserver`

## Database Preparation
- [ ] Create PostgreSQL database on Render.com (or your hosting provider)
- [ ] Get the DATABASE_URL connection string
- [ ] Ensure database supports SSL connections

## Environment Variables to Configure
On your hosting platform's environment variable settings, add:

### Required Variables
- [ ] `SECRET_KEY` - Generate with: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
- [ ] `DEBUG=False`
- [ ] `DATABASE_URL=postgresql://...` (from your database setup)

### Security Variables (Adjust for Your Domain)
- [ ] `ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-app.onrender.com`
- [ ] `CORS_ALLOWED_ORIGINS=https://your-frontend.onrender.com,https://yourdomain.com`
- [ ] `CSRF_TRUSTED_ORIGINS=https://your-frontend.onrender.com,https://yourdomain.com`

### Optional - Render Deployment
- [ ] `RENDER_EXTERNAL_HOSTNAME=your-app.onrender.com` (auto-set by Render)

### Optional - Email Configuration
- [ ] `EMAIL_HOST=smtp.gmail.com`
- [ ] `EMAIL_PORT=587`
- [ ] `EMAIL_HOST_USER=your-email@gmail.com`
- [ ] `EMAIL_HOST_PASSWORD=your-app-specific-password`
- [ ] `DEFAULT_FROM_EMAIL=noreply@yourdomain.com`

### Optional - Superuser Creation
- [ ] `CREATE_SUPERUSER=True`
- [ ] `DJANGO_SUPERUSER_USERNAME=admin`
- [ ] `DJANGO_SUPERUSER_EMAIL=admin@yourdomain.com`
- [ ] `DJANGO_SUPERUSER_PASSWORD=secure-password-here`

## Deployment Platform Configuration

### For Render.com:
- [ ] Create new "Web Service"
- [ ] Connect Git repository
- [ ] Set Python version to 3.11 (or higher)
- [ ] Add all environment variables (see above)
- [ ] Build Command: `./build.sh`
- [ ] Start Command: `gunicorn backend.wsgi`
- [ ] Click "Create Web Service"

### For Heroku:
- [ ] Create new Heroku app
- [ ] Connect Git repository
- [ ] Set environment variables using `heroku config:set`
- [ ] Deploy: `git push heroku main`

### For Other Platforms:
- [ ] Install Python 3.11+
- [ ] Install PostgreSQL
- [ ] Set all environment variables
- [ ] Run: `./build.sh`
- [ ] Start with: `gunicorn backend.wsgi`

## Post-Deployment Verification
- [ ] Check deployment logs for errors
- [ ] Verify static files are served: Visit `/admin/` 
- [ ] Test API endpoints:
  - [ ] `GET /api/services/` - Should return JSON list (no auth required)
  - [ ] `POST /api/auth/login/` - Should return error for invalid creds
  - [ ] `GET /api/auth/user/` - Should return 401 (unauthorized)
- [ ] Check Django admin: `/admin/` with superuser credentials
- [ ] Ensure HTTPS is working (should auto-redirect)

## Common Issues & Quick Fixes

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Database Connection Error
- [ ] Verify DATABASE_URL is correct
- [ ] Check database credentials
- [ ] Ensure SSL is enabled for PostgreSQL

### Migrations Error
- [ ] Check `__init__.py` exists in migrations folders
- [ ] View migration status: `python manage.py showmigrations`

### Superuser Access Issues
- [ ] Verify DJANGO_SUPERUSER_PASSWORD is set
- [ ] Try creating manually if needed:
  ```bash
  python manage.py createsuperuser
  ```

## 📞 Monitor After Deployment
- [ ] Set up error tracking (Sentry recommended)
- [ ] Monitor database performance
- [ ] Monitor server logs regularly
- [ ] Set up backup schedule

## ✅ Final Checks Before Going Live
- [ ] All environment variables correctly set
- [ ] Database migrations successful
- [ ] Static files serving correctly
- [ ] API endpoints responding
- [ ] HTTPS working
- [ ] Admin panel accessible
- [ ] Frontend can connect to backend
- [ ] Email working (if configured)

---

**Status**: Ready for Deployment ✅
**Last Updated**: February 28, 2026
**Python Version**: 3.11.7
**Django Version**: 4.2.9
