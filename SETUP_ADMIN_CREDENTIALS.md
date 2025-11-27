# 🔐 Setup Admin Login Credentials

## How It Works

The `create_superuser.py` script automatically creates a superuser account on first deployment if one doesn't exist.

## Set Credentials via Environment Variables

You need to set these environment variables in your Render dashboard:

### Step 1: Go to Environment Variables

1. **Open your Render dashboard**
2. **Go to your service**: `my-personal-blog`
3. **Click "Environment" tab**
4. **Add these variables:**

### Step 2: Add Required Variables

Click "Add Environment Variable" for each:

#### 1. ADMIN_USERNAME (Optional)
- **Key**: `ADMIN_USERNAME`
- **Value**: `admin` (or your preferred username)
- **Default**: If not set, uses `admin`

#### 2. ADMIN_EMAIL (Optional)
- **Key**: `ADMIN_EMAIL`
- **Value**: `your-email@example.com`
- **Default**: If not set, uses `admin@example.com`

#### 3. ADMIN_PASSWORD (Required)
- **Key**: `ADMIN_PASSWORD`
- **Value**: `YourSecurePassword123!` (choose a strong password)
- **Default**: If not set, uses `changeme123` ⚠️ **CHANGE THIS!**

### Step 3: Deploy

After adding environment variables:

1. **Go to "Events" tab**
2. **Click "Manual Deploy"**
3. **Select "Deploy latest commit"**
4. **Wait for deployment**

### Step 4: Check Logs

After deployment, check logs. You should see:
```
Creating superuser (if needed)...
✅ Superuser 'admin' created successfully!
   Email: admin@example.com
   Password: YourSecurePassword123!
```

## Login Credentials

After first deployment, use:

### Default Credentials (if you didn't set environment variables):
- **Username**: `admin`
- **Email**: `admin@example.com`
- **Password**: `changeme123`

⚠️ **IMPORTANT**: Change the password immediately after first login!

### Custom Credentials:
Use the values you set in the `ADMIN_USERNAME` and `ADMIN_PASSWORD` environment variables.

## How to Login

1. **Visit**: `https://my-personal-blog-4wb8.onrender.com/admin/`
2. **Enter your credentials**
3. **Click "Log in"**

## Change Password After First Login

1. **Login to admin panel**
2. **Click on your username** (top right)
3. **Click "Change password"**
4. **Enter new password twice**
5. **Click "Change my password"**

## Security Notes

- ⚠️ The script only creates the superuser if it doesn't exist
- ✅ Safe to run multiple times (won't create duplicate users)
- ✅ After creation, you can remove the `ADMIN_PASSWORD` from environment variables if you want
- ⚠️ **Always change the default password immediately!**

## Troubleshooting

### Can't Login?

1. **Check logs** to see if superuser was created
2. **Verify environment variables** are set correctly
3. **Try the default credentials**: `admin` / `changeme123`
4. **Check if migrations ran successfully** (user table needs to exist)

### Want to Create Another Superuser?

You can create additional superusers through the admin panel:
1. Login as admin
2. Go to "Users" → "Add user"
3. Create the user
4. Check "Staff status" and "Superuser status"
5. Save

### Reset Admin Password

If you forgot the password, you can update it:
1. Set `ADMIN_PASSWORD` environment variable to a new password
2. Delete the existing admin user (or use Django shell if available)
3. Redeploy - the script will create a new admin with the new password

Or add this temporary code to reset:

```python
# In Django shell or management command
from django.contrib.auth import get_user_model
User = get_user_model()
admin = User.objects.get(username='admin')
admin.set_password('new_password')
admin.save()
```

