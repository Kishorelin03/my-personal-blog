# Fix: Posts Not Saving (Database Persistence Issue)

## Problem
Your blog posts are being created but disappear after a day or when the app restarts. This happens because **SQLite is being used instead of PostgreSQL**.

On Render's free tier, the filesystem is **ephemeral** - meaning SQLite database files get wiped every time:
- The app restarts
- The app redeploys
- The app goes to sleep (after 15 minutes of inactivity)
- Render performs maintenance

## Solution: Use PostgreSQL Database

You **MUST** use PostgreSQL on Render because it's a persistent, managed database service. SQLite files are stored on the filesystem and get deleted.

## Step-by-Step Fix

### Option 1: Using Render Blueprint (Recommended)

Your `render.yaml` file already includes a PostgreSQL database configuration. If you deployed using the blueprint, the database should already exist.

1. **Check if Database Exists:**
   - Go to your Render dashboard: https://dashboard.render.com
   - Look for a service named `kishorelinblog-db` (PostgreSQL database)
   - If it exists, proceed to step 2
   - If it doesn't exist, see Option 2 below

2. **Verify Database Connection:**
   - In your web service (`kishorelinblog`), go to the "Environment" tab
   - Check if `DATABASE_URL` environment variable exists
   - It should have a value like: `postgresql://user:password@host:port/database`
   - If it's missing, the database isn't connected to your web service

3. **Connect Database to Web Service:**
   - Go to your PostgreSQL database service (`kishorelinblog-db`)
   - Click on "Connections" tab
   - Under "Internal Connections", you should see your web service listed
   - If not, click "Connect" and select your web service (`kishorelinblog`)

4. **Redeploy Your Web Service:**
   - Go to your web service
   - Click "Manual Deploy" → "Deploy latest commit"
   - This will restart your app with the PostgreSQL database

### Option 2: Create Database Manually (If Blueprint Didn't Create It)

1. **Create PostgreSQL Database:**
   - Go to Render dashboard: https://dashboard.render.com
   - Click "New +" → "PostgreSQL"
   - Name: `kishorelinblog-db`
   - Database: `kishorelinblog`
   - User: `kishorelinblog`
   - Region: Choose closest to you
   - Plan: **Free**
   - Click "Create Database"

2. **Connect Database to Web Service:**
   - In the database service, go to "Connections" tab
   - Under "Internal Connections", click "Connect"
   - Select your web service (`kishorelinblog`)

3. **Verify Environment Variable:**
   - Go to your web service (`kishorelinblog`)
   - Go to "Environment" tab
   - Check that `DATABASE_URL` exists and has a value
   - It should automatically be set when you connect the database

4. **Redeploy:**
   - Go to your web service
   - Click "Manual Deploy" → "Deploy latest commit"

### Option 3: Manual Environment Variable Setup

If the automatic connection didn't work:

1. **Get Database Connection String:**
   - Go to your PostgreSQL database service
   - In the "Connections" tab, copy the "Internal Database URL"
   - It looks like: `postgresql://user:password@hostname:5432/database`

2. **Set Environment Variable:**
   - Go to your web service (`kishorelinblog`)
   - Go to "Environment" tab
   - Click "Add Environment Variable"
   - Key: `DATABASE_URL`
   - Value: Paste the internal database URL you copied
   - Click "Save Changes"

3. **Redeploy:**
   - Click "Manual Deploy" → "Deploy latest commit"

## Verification

After redeploying, check the logs:

1. Go to your web service on Render
2. Click on "Logs" tab
3. Look for these messages:
   ```
   ✅ Using PostgreSQL database from DATABASE_URL
   Database: kishorelinblog
   ✅ Database connection successful!
   ```

If you see warnings like:
```
⚠️  WARNING: Running on Render but DATABASE_URL not found!
⚠️  Using SQLite as fallback (DATA WILL BE LOST ON DEPLOY/RESTART!)
```

This means the database isn't connected. Follow the steps above to fix it.

## After Fix

Once PostgreSQL is connected:

1. **Create Admin User:**
   - The superuser will be created automatically on deploy
   - Username: `aruldha`
   - Email: `aruldha@uwindsor.ca`
   - Password: `Arulmabel@95`

2. **Test:**
   - Create a blog post
   - Wait a few minutes (or trigger a redeploy)
   - Check if the post still exists
   - Your posts should now persist!

## Important Notes

- **Free Tier Limitation:** On Render's free tier, your database goes to sleep after 90 days of inactivity. When it wakes up, it takes about 1 minute. Your data is still safe!

- **Backup:** Render automatically backs up your PostgreSQL database. You can download backups from the database service dashboard.

- **Local Development:** SQLite is fine for local development. The issue only occurs on Render because of the ephemeral filesystem.

## Troubleshooting

**Problem:** `OperationalError: FATAL: database does not exist`
- Solution: Make sure the database name in `render.yaml` matches the actual database name

**Problem:** `OperationalError: FATAL: password authentication failed`
- Solution: The database connection string might be incorrect. Re-connect the database service to the web service.

**Problem:** Still using SQLite after connecting database
- Solution: 
  1. Check that `DATABASE_URL` environment variable is set in your web service
  2. Check the logs to see which database is being used
  3. Make sure `dj-database-url` is in `requirements.txt` (it is!)
  4. Redeploy your service

## Summary

**The root cause:** SQLite files get deleted on Render's ephemeral filesystem.

**The solution:** Use PostgreSQL (persistent managed database).

**What changed:** The code now:
- Detects if running on Render
- Warns if DATABASE_URL is missing
- Verifies database connection on startup
- Logs which database is being used

Your `render.yaml` already has the database configuration. You just need to ensure the database service exists and is connected to your web service!

