# 🔧 Fix Database Connection on Render

## Problem
Your app is using SQLite instead of PostgreSQL, causing `no such table` errors.

## Root Cause
The `DATABASE_URL` environment variable isn't being set or read correctly.

## Solution: Manually Set DATABASE_URL

Since `render.yaml` might not be automatically applied (depending on how you set up the service), you need to manually configure the database connection.

### Step 1: Get Your PostgreSQL Connection String

1. **Go to Render Dashboard**
2. **Click on your database**: `kishorelinblog-db`
3. **Go to "Connections" tab** (or "Info" tab)
4. **Copy the "Internal Database URL"** or "Connection String"
   - It should look like: `postgresql://kishorelinblog:password@dpg-xxxxx-a/kishorelinblog`

### Step 2: Set DATABASE_URL Environment Variable

1. **Go to your web service**: `my-personal-blog`
2. **Click "Environment" tab** (left sidebar)
3. **Click "Add Environment Variable"** button
4. **Add:**
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the connection string you copied
5. **Click "Save Changes"**

### Step 3: Ensure Migrations Run

The service needs to be configured with the pre-deploy command. Check:

1. **Go to "Settings" tab**
2. **Scroll to "Build & Deploy" section**
3. **Ensure "Pre-Deploy Command" is set to:**
   ```
   python manage.py migrate --noinput
   ```
4. **If not set, add it and click "Save Changes"**

### Step 4: Trigger Manual Deploy

1. **Go to "Events" tab**
2. **Click "Manual Deploy"**
3. **Select "Deploy latest commit"**
4. **Wait for deployment** (check logs to see migrations running)

### Step 5: Verify Database Connection

Check the logs during deployment. You should see:
- ✅ `Operations to perform: Apply all migrations...`
- ✅ `Applying BlogApp.0001_initial... OK`
- ✅ No SQLite errors

## Alternative: Use Render Blueprint

If you want to use `render.yaml` automatically:

1. **Delete the current service** (or start fresh)
2. **Go to Render Dashboard**
3. **Click "New +" → "Blueprint"**
4. **Connect your GitHub repo**
5. **Render will automatically use `render.yaml`**
6. **This will set up both service and database with correct connections**

## Quick Check: Current Environment Variables

To see what's currently set:
1. Go to your service → "Environment" tab
2. Check if `DATABASE_URL` exists
3. If not, add it using the steps above

## After Fix: Create Superuser

Once migrations run successfully, create an admin account:

Since Shell is locked on free tier, create superuser via one-time job or use Django management command through Render Jobs (if available).

Or temporarily add this to your code to auto-create admin (remove after first use):
```python
# In BlogApp/views.py or manage.py (temporary!)
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'your-password')
```

