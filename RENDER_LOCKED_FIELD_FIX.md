# 🔓 Fix Locked Fields in Render Dashboard

## Why Fields Are Locked

The fields are locked because Render detects the `render.yaml` file in your repository. This is actually **good** - it means Render is using infrastructure-as-code!

## Solution Options

### Option 1: Let render.yaml Handle It (Recommended)

The `render.yaml` file I just updated already has the `preDeployCommand` set to run migrations automatically. Just:

1. **Wait for auto-deploy** - Render will detect the updated `render.yaml` and redeploy
2. **OR manually trigger deploy**:
   - Go to your service → "Events" tab
   - Click "Manual Deploy" → "Deploy latest commit"

The migrations will run automatically during deployment.

### Option 2: Remove render.yaml to Use UI (Alternative)

If you prefer using the UI instead:

1. **Delete render.yaml from your repo**:
   ```bash
   git rm render.yaml
   git commit -m "Remove render.yaml to use UI configuration"
   git push
   ```

2. **Then configure in UI**:
   - Fields will unlock
   - Add Pre-Deploy Command: `python manage.py migrate --noinput`
   - Configure all settings in the dashboard

### Option 3: Run Migrations Manually (Quick Fix)

If you need it working **right now**:

1. Go to your service in Render dashboard
2. Click **"Shell"** tab (in the left sidebar)
3. Run:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
4. This creates tables immediately (one-time fix)

## Recommended: Use render.yaml (Option 1)

The `render.yaml` file I updated will:
- ✅ Automatically run migrations before each deploy
- ✅ Connect to PostgreSQL database
- ✅ Set all environment variables
- ✅ Make your deployment reproducible

Just wait for the next deploy (automatic) or trigger it manually.

## Current render.yaml Configuration

The file now includes:
- `preDeployCommand: python manage.py migrate --noinput` ✅
- Database connection via `fromDatabase` ✅
- All necessary environment variables ✅

This means migrations will run automatically on every deployment!


