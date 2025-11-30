# 🆓 Free Tier Setup Guide for Render

## Problem
Render's free tier doesn't support `preDeployCommand`, so migrations won't run automatically.

## Solution: Use Startup Script

We've created a `start.sh` script that:
1. Runs migrations automatically when the server starts
2. Collects static files
3. Starts the Gunicorn server

## Setup Steps

### Step 1: Update Your Service Settings

Since you can't edit `render.yaml` fields on free tier, manually update in Render dashboard:

1. **Go to your service**: `my-personal-blog`
2. **Click "Settings" tab**
3. **Scroll to "Build & Deploy" section**
4. **Update "Start Command"** to:
   ```
   chmod +x start.sh && ./start.sh
   ```
5. **Keep "Build Command"** as:
   ```
   pip install -r requirements.txt && python manage.py collectstatic --noinput
   ```
6. **Click "Save Changes"**

### Step 2: Set DATABASE_URL Environment Variable

**CRITICAL**: You must manually set the database connection:

1. **Go to your database**: `kishorelinblog-db`
2. **Go to "Info" or "Connections" tab**
3. **Copy the "Internal Database URL"**
   - Format: `postgresql://user:password@host/database`
4. **Go back to your web service**: `my-personal-blog`
5. **Click "Environment" tab**
6. **Add new variable**:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the connection string
7. **Click "Save Changes"**

### Step 3: Trigger Manual Deploy

1. **Go to "Events" tab**
2. **Click "Manual Deploy"**
3. **Select "Deploy latest commit"**
4. **Wait for deployment**

### Step 4: Check Logs

After deployment, check the logs. You should see:
```
Running database migrations...
Operations to perform:
  Apply all migrations: ...
Running migrations:
  Applying BlogApp.0001_initial... OK
Collecting static files...
Starting server...
```

## What the Startup Script Does

The `start.sh` script:
- ✅ Runs migrations on every server start (safe, Django only applies new migrations)
- ✅ Collects static files (as backup, though build command also does this)
- ✅ Starts Gunicorn server

**Note**: Running migrations on startup is safe because Django only applies new migrations. If no new migrations exist, it does nothing.

## Alternative: Run Migrations in Build Command

If the startup script doesn't work, you can add migrations to the build command:

**Build Command**:
```
pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

**Start Command**:
```
gunicorn KishorelinBlog.wsgi:application
```

However, the startup script approach is better because:
- Migrations run on every deploy (when server starts)
- More reliable on free tier

## Verify Everything Works

1. **Check logs** for migration output
2. **Visit your site**: `https://my-personal-blog-4wb8.onrender.com`
3. **Should work without errors!**

## Create Admin User

After migrations run, you need to create a superuser. Since Shell is locked on free tier:

### Option 1: Use Django Management Command (Temporary Code)

Temporarily add this to your `BlogApp/views.py` or create a management command:

```python
# Temporary - remove after creating admin
from django.contrib.auth import get_user_model

def create_admin():
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'your-password')
        print("Admin user created!")
    else:
        print("Admin user already exists")

# Call this once in a view or management command
```

### Option 2: Use Render Jobs (If Available)

Some Render accounts have access to one-time jobs even on free tier. Check if you see "Jobs" in your dashboard.

## Troubleshooting

### Still Getting SQLite Errors?

- ✅ Check that `DATABASE_URL` is set in Environment variables
- ✅ Verify the connection string is correct (should start with `postgresql://`)
- ✅ Check logs to see if migrations ran

### Migrations Not Running?

- ✅ Check that `start.sh` has execute permissions (should be set by `chmod +x start.sh`)
- ✅ Check logs for any errors during startup
- ✅ Verify the start command is correct: `chmod +x start.sh && ./start.sh`


