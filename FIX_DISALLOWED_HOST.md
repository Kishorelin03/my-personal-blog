# 🔧 Fix DisallowedHost Error on Render

## Quick Fix

You're seeing this error because `my-personal-blog-4wb8.onrender.com` is not in `ALLOWED_HOSTS`.

### Option 1: Update Environment Variable (Recommended)

1. Go to your Render dashboard
2. Click on your web service: `my-personal-blog`
3. Go to "Environment" tab
4. Find `ALLOWED_HOSTS` variable
5. Update the value to:
   ```
   my-personal-blog-4wb8.onrender.com,*.onrender.com,localhost,127.0.0.1
   ```
6. Click "Save Changes"
7. Render will automatically redeploy

### Option 2: Use RENDER_EXTERNAL_HOSTNAME (Automatic)

I've updated the code to automatically detect Render domains. Just make sure:

1. In Render dashboard → Your service → Environment
2. The `ALLOWED_HOSTS` variable is either:
   - Not set at all (code will auto-detect), OR
   - Set to: `*.onrender.com,localhost,127.0.0.1`

### Option 3: Manual Fix (If auto-detection doesn't work)

Set `ALLOWED_HOSTS` environment variable in Render to:
```
my-personal-blog-4wb8.onrender.com
```

Or use wildcard:
```
*.onrender.com
```

## After Updating

1. Save the environment variable in Render
2. Wait for automatic redeploy (or manually trigger deploy)
3. Visit your site again: `https://my-personal-blog-4wb8.onrender.com`
4. The error should be gone!

## What I Updated in Code

The `settings.py` now automatically detects Render domains using `RENDER_EXTERNAL_HOSTNAME` environment variable that Render sets automatically. This means you don't need to manually update `ALLOWED_HOSTS` every time Render assigns a new subdomain.


