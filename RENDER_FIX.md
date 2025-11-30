# 🔧 Fix Your Render Configuration

## ❌ Problem
Your Build Command and Start Command have the wrong format.

## ✅ Correct Configuration

### Build Command
**Remove** the `KishorelinBlog/ $` prefix. Should be:
```
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

### Start Command  
**Remove** the `KishorelinBlog/ $` prefix. Should be:
```
gunicorn KishorelinBlog.wsgi:application
```

## Complete Configuration Checklist

✅ **Language**: Python 3 (Correct!)
✅ **Branch**: main (Correct!)
✅ **Region**: Oregon (US West) (Correct!)
✅ **Root Directory**: KishorelinBlog (Correct!)
❌ **Build Command**: Remove `KishorelinBlog/ $` prefix
❌ **Start Command**: Remove `KishorelinBlog/ $` prefix
❓ **Instance Type**: Select "Free"
❓ **Environment Variables**: Need to add (see below)

## Environment Variables (Click "Advanced" button)

Add these in the Environment Variables section:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | `b+izf3_99&o2$$%r36x=rsn&w_v1ve4f*&zm@xssyfe!^bn9d5` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `kishorelinblog.onrender.com` (or your service name) |
| `PYTHON_VERSION` | `3.11.0` |

## Important: Create Database First!

1. Go back to Render dashboard (click "Render" logo or "Home")
2. Click "New +" → "PostgreSQL"
3. Name: `kishorelinblog-db`
4. Plan: `Free`
5. Region: `Oregon (US West)` (same as web service)
6. Click "Create Database"
7. After creation, copy the **Internal Database URL**
8. Go back to your Web Service configuration
9. Add environment variable:
   - Key: `DATABASE_URL`
   - Value: (paste the Internal Database URL)

## Final Steps

1. Fix Build Command and Start Command (remove prefixes)
2. Select Instance Type: **Free**
3. Add all environment variables
4. Scroll down and click **"Create Web Service"**

The commands should NOT have the `KishorelinBlog/ $` prefix - that's just Render's UI indicator showing where commands run, but shouldn't be in the actual command text.


