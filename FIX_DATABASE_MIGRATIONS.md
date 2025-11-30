# 🔧 Fix "no such table" Database Error on Render

## Problem
The error `no such table: BlogApp_blogpost` means database migrations haven't been run yet.

Also, the error shows it's using SQLite3 (`/opt/render/project/src/.venv/lib/python3.13/site-packages/django/db/backends/sqlite3/base.py`), which means your PostgreSQL database isn't connected yet.

## Solution: Two Steps

### Step 1: Connect PostgreSQL Database

1. **In Render Dashboard:**
   - Make sure you have a PostgreSQL database created
   - Go to your database: `kishorelinblog-db`
   - Copy the **Internal Database URL**

2. **Link Database to Web Service:**
   - Go to your web service: `my-personal-blog`
   - Go to "Environment" tab
   - Add environment variable:
     - **Key**: `DATABASE_URL`
     - **Value**: Paste the Internal Database URL from step 1
   - Click "Save Changes"

### Step 2: Run Database Migrations

You have two options:

#### Option A: Use Pre-Deploy Command (Recommended - Automatic)

1. Go to your web service in Render
2. Go to "Settings" tab
3. Scroll to "Pre-Deploy Command"
4. Add this command:
   ```
   python manage.py migrate --noinput
   ```
5. Click "Save Changes"
6. Render will redeploy automatically and run migrations

#### Option B: Run Manually via Shell (One-time)

1. Go to your web service in Render
2. Click "Shell" tab (or "Logs" → "Shell")
3. Run these commands:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
4. This creates all tables and sets up your admin account

## Quick Fix Checklist

- [ ] PostgreSQL database created in Render
- [ ] `DATABASE_URL` environment variable set (Internal Database URL)
- [ ] Pre-Deploy Command set to: `python manage.py migrate --noinput`
- [ ] Service redeployed (automatic if you save changes)

## Verify It's Working

After redeploy:
1. Visit: `https://my-personal-blog-4wb8.onrender.com`
2. You should see your homepage (even if no posts yet)
3. Visit: `https://my-personal-blog-4wb8.onrender.com/admin`
4. Login and create your first blog post!

## Why SQLite Instead of PostgreSQL?

The error shows SQLite because `DATABASE_URL` environment variable is not set. Once you set it, Django will automatically use PostgreSQL instead of SQLite.


