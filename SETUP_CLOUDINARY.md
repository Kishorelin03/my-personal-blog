# Setup Cloudinary for Image Storage

## Problem
On Render's free tier, the filesystem is **ephemeral**. Uploaded images are stored locally and get **deleted** when:
- The instance spins down (after 15 minutes of inactivity)
- The instance restarts
- The app redeploys

This is why your images disappear after 15 minutes even though the database content persists.

## Solution: Cloudinary
Cloudinary is a cloud-based image management service with a **generous free tier**:
- ✅ 25 GB storage
- ✅ 25 GB monthly bandwidth
- ✅ Automatic image optimization
- ✅ CDN delivery (fast image loading)
- ✅ Free forever (no credit card required for free tier)

## Step 1: Create Cloudinary Account

1. Go to https://cloudinary.com/users/register/free
2. Sign up with your email (free account)
3. Verify your email address
4. You'll be taken to the Dashboard

## Step 2: Get Your Cloudinary Credentials

1. In the Cloudinary Dashboard, you'll see your **Account Details** (or go to Settings → Product environment credentials)
2. Copy these three values:
   - **Cloud name** (e.g., `dk5x7abcd`)
   - **API Key** (e.g., `123456789012345`)
   - **API Secret** (e.g., `abcdefghijklmnopqrstuvwxyz123456`)

⚠️ **Keep these credentials secret!** Never commit them to git.

## Step 3: Set Environment Variables on Render

1. Go to your Render dashboard: https://dashboard.render.com
2. Click on your web service (`my-personal-blog`)
3. Go to the **"Environment"** tab
4. Click **"Add Environment Variable"** and add these three variables:

   **Variable 1:**
   - Key: `CLOUDINARY_CLOUD_NAME`
   - Value: Your Cloudinary cloud name (e.g., `dk5x7abcd`)
   - Click "Save Changes"

   **Variable 2:**
   - Key: `CLOUDINARY_API_KEY`
   - Value: Your Cloudinary API key (e.g., `123456789012345`)
   - Click "Save Changes"

   **Variable 3:**
   - Key: `CLOUDINARY_API_SECRET`
   - Value: Your Cloudinary API secret (e.g., `abcdefghijklmnopqrstuvwxyz123456`)
   - Click "Save Changes"

5. After adding all three variables, Render will automatically redeploy your service.

## Step 4: Verify It's Working

After redeploy, check the logs:

1. Go to your web service on Render
2. Click on **"Logs"** tab
3. Look for this message:
   ```
   ✅ Using Cloudinary for media file storage (images will persist)
   ```

If you see warnings instead:
```
⚠️  WARNING: Using local filesystem for media files!
⚠️  Images will be LOST when the instance spins down!
```

This means the environment variables aren't set correctly. Double-check:
- All three variables are set (CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET)
- Variable names are exactly as shown (case-sensitive)
- Values are correct (no extra spaces)

## Step 5: Test

1. Upload a new image through your blog post form
2. Wait a few minutes (or trigger a redeploy)
3. Check if the image still loads
4. **Your images should now persist!** 🎉

## What Changed?

- **Before**: Images stored in `/media/` folder on Render's ephemeral filesystem → **DELETED on restart**
- **After**: Images stored on Cloudinary cloud → **PERSISTENT, accessible from anywhere**

## Local Development

For local development, images will still be stored locally (in the `media/` folder). Cloudinary is only used when:
- Running on Render (`IS_RENDER = True`)
- All three Cloudinary environment variables are set

This way, you don't need Cloudinary credentials to develop locally!

## Free Tier Limits

Cloudinary's free tier includes:
- 25 GB storage (plenty for thousands of images)
- 25 GB monthly bandwidth
- Automatic image optimization and transformation
- CDN delivery

For most personal blogs, the free tier is more than enough!

## Troubleshooting

**Problem**: Images still disappearing after setup
- **Solution**: Check that all three environment variables are set correctly in Render
- Verify in logs that Cloudinary is being used (look for the ✅ message)

**Problem**: Can't see images after upload
- **Solution**: Clear your browser cache and try again
- Check the image URL in the browser - it should point to `res.cloudinary.com`

**Problem**: "Invalid credentials" error
- **Solution**: Double-check your Cloudinary credentials in the dashboard
- Make sure there are no extra spaces in the environment variable values

## Summary

1. ✅ Create free Cloudinary account
2. ✅ Copy credentials (cloud name, API key, API secret)
3. ✅ Add three environment variables in Render
4. ✅ Wait for redeploy
5. ✅ Verify in logs
6. ✅ Upload test image
7. ✅ Celebrate! 🎉 Images now persist forever!

