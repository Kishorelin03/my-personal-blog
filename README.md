# KishorelinBlog - Personal Blog Platform

A personal blogging platform built with Django and Bootstrap.

## 📁 Project Structure

```
KishorelinBlog/
├── BlogApp/              # Django app for blog functionality
├── KishorelinBlog/       # Django project settings
├── templates/            # HTML templates (Bootstrap)
├── static/               # Static files
├── media/                # Media uploads
├── db.sqlite3           # SQLite database (development)
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
└── venv/                # Python virtual environment
```

## 🚀 Quick Start

### Setup

1. **Navigate to project directory:**
   ```bash
   cd KishorelinBlog
   ```

2. **Activate virtual environment:**
   ```bash
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies (if not already installed):**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start Django server:**
   ```bash
   python manage.py runserver
   ```
   
   Application will run at: `http://127.0.0.1:8000`

## 🔐 Access

- **Homepage**: `http://127.0.0.1:8000/`
- **Blog**: `http://127.0.0.1:8000/blog/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`
- **Dashboard**: `http://127.0.0.1:8000/dashboard/` (staff only)
- **API**: `http://127.0.0.1:8000/api/`

## 📝 Features

### Author Features (Admin Only)
- Create, edit, delete blog posts via Django Admin or Dashboard
- Save posts as draft or publish
- Upload cover images
- Add tags and categories
- Auto-generate URL slugs
- Dashboard with analytics (views, likes, comments, monthly stats)

### Public/Reader Features
- Browse blog posts
- Search and filter posts
- View post details
- Like posts (no login required, session-based)
- Comment on posts
- Bookmark/Save posts (login required)

## 🛠 Tech Stack

- **Backend**: Django 5+
- **Frontend**: Bootstrap 5
- **Database**: SQLite (development)
- **API**: Django REST Framework (available at `/api/`)

## 📦 Dependencies

See `requirements.txt` for Python dependencies including:
- Django 5+
- Django REST Framework
- django-cors-headers
- Pillow (for image handling)

## 📄 Pages

### Public Pages
- `/` - Homepage with featured and latest posts
- `/blog/` - Blog listing with search and filters
- `/blog/<slug>/` - Blog post detail
- `/about/` - About/portfolio page
- `/projects/` - Projects showcase
- `/contact/` - Contact form

### Admin Pages
- `/dashboard/` - Admin dashboard with analytics
- `/dashboard/posts/` - Manage all posts
- `/dashboard/new/` - Create new post
- `/dashboard/edit/<id>/` - Edit post
- `/admin/` - Django admin panel

## 🌐 API Endpoints (Optional)

REST API is available at `/api/`:
- `/api/posts/` - List/create posts
- `/api/posts/<slug>/` - Post detail
- `/api/comments/` - Comments
- `/api/categories/` - Categories
- `/api/tags/` - Tags
- `/api/dashboard/stats/` - Dashboard statistics

## 🎨 UI Features

- **Bootstrap 5** with custom styling
- **Dark mode toggle**
- **Responsive design** (mobile-friendly)
- **Clean, modern interface**
- **Font Awesome icons**

## 📄 License

Personal project - All rights reserved

## 👤 Author

KishorelinBlog
