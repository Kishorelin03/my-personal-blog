# 🚀 Render Quick Setup Guide

## Step-by-Step Render Configuration

When you see the "New Web Service" page, here's exactly what to fill in:

### 1. **Basic Settings** (at the top of the page)
- **Name**: `kishorelinblog` (or any name you prefer)
- **Region**: Choose closest to you (e.g., `Oregon (US West)`)
- **Branch**: `main`
- **Root Directory**: `KishorelinBlog` (important! Your Django project is in this folder)

### 2. **Environment**
- **Environment**: `Python 3`
- **Python Version**: `3.11` (or latest available)

### 3. **Build & Deploy**
- **Build Command**: 
  ```
  pip install -r requirements.txt && python manage.py collectstatic --noinput
  ```

- **Start Command**: 
  ```
  gunicorn KishorelinBlog.wsgi:application
  ```

### 4. **Pre-Deploy Command** (the section you see in the image)
```
python manage.py migrate --noinput
```
*(This runs database migrations before starting the service)*

### 5. **Plan**
- **Instance Type**: `Free`

### 6. **Environment Variables** (Click "Advanced" or scroll down)
Add these environment variables:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | *(Generate a new one - see below)* |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `kishorelinblog.onrender.com` (or your service name) |
| `PYTHON_VERSION` | `3.11.0` |

### 7. **Create PostgreSQL Database First!**
Before creating the web service, you need to:
1. Go back to Render dashboard
2. Click "New +" → "PostgreSQL"
3. **Name**: `kishorelinblog-db`
4. **Plan**: `Free`
5. **Region**: Same as your web service
6. After creating, copy the **Internal Database URL**
7. Add environment variable:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the Internal Database URL

## Generate SECRET_KEY

Run this command in your terminal:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it as the `SECRET_KEY` environment variable value.

## Complete Configuration Summary

**Required Fields:**
- ✅ Name: `kishorelinblog`
- ✅ Root Directory: `KishorelinBlog`
- ✅ Environment: `Python 3`
- ✅ Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- ✅ Start Command: `gunicorn KishorelinBlog.wsgi:application`
- ✅ Plan: `Free`

**Required Environment Variables:**
- ✅ `SECRET_KEY` (generate new one)
- ✅ `DEBUG` = `False`
- ✅ `ALLOWED_HOSTS` = `your-service-name.onrender.com`
- ✅ `DATABASE_URL` (from PostgreSQL database)

**Optional but Recommended:**
- Pre-Deploy Command: `python manage.py migrate --noinput`

## After Deployment

1. **Wait for build** (5-10 minutes)
2. **Check logs** if deployment fails
3. **Run migrations manually** if needed:
   - Go to your service → "Shell" tab
   - Run: `python manage.py migrate`
4. **Create superuser**:
   - In Shell: `python manage.py createsuperuser`
5. **Visit your site**: `https://your-service-name.onrender.com`

## Troubleshooting

If you see errors:
- **Check logs**: Service → "Logs" tab
- **Verify Root Directory**: Should be `KishorelinBlog` (not the repo root)
- **Check environment variables**: Make sure all are set correctly
- **Database connection**: Ensure `DATABASE_URL` is set correctly

## Your Deployed URLs

- **Website**: `https://your-service-name.onrender.com`
- **Admin Panel**: `https://your-service-name.onrender.com/admin`


