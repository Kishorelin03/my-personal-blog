from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from collections import defaultdict

from .models import BlogPost, Comment, Like, SavedPost, ContactMessage, Category, Tag, AboutPage, ContactPage
from .forms import BlogPostForm, CommentForm, ContactForm


def is_author(user):
    """Check if user is staff (author/admin)"""
    return user.is_authenticated and user.is_staff


# Authentication Views

def user_login(request):
    """Custom login view"""
    # If user is already logged in, redirect to dashboard
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard')
        else:
            return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.username}!')
                    # Redirect staff users to dashboard, others to home
                    if user.is_staff:
                        return redirect('dashboard')
                    else:
                        return redirect('home')
                else:
                    messages.error(request, 'Your account is disabled.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please provide both username and password.')
    
    return render(request, 'login.html')


def user_logout(request):
    """Custom logout view"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')


# Public Views

def home(request):
    """Homepage with featured and latest posts"""
    featured_posts = BlogPost.objects.filter(is_published=True, is_featured=True)[:3]
    # Get featured post IDs for exclusion
    featured_ids = list(featured_posts.values_list('id', flat=True))
    latest_posts = BlogPost.objects.filter(is_published=True).exclude(id__in=featured_ids)[:6]
    
    # Get stats for hero section
    total_posts = BlogPost.objects.filter(is_published=True).count()
    total_views = BlogPost.objects.filter(is_published=True).aggregate(Sum('view_count'))['view_count__sum'] or 0
    total_likes = Like.objects.count()
    
    context = {
        'featured_posts': featured_posts,
        'latest_posts': latest_posts,
        'total_posts': total_posts,
        'total_views': total_views,
        'total_likes': total_likes,
    }
    return render(request, 'home.html', context)


def blog_list(request):
    """Blog listing with search and filters"""
    posts = BlogPost.objects.filter(is_published=True).select_related('author', 'category').prefetch_related('tags')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct()
    
    # Filter by category
    category_slug = request.GET.get('category', '')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    # Filter by tag
    tag_slug = request.GET.get('tag', '')
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
    
    # Filter by date
    date_filter = request.GET.get('date', '')
    if date_filter == 'today':
        posts = posts.filter(created_at__date=timezone.now().date())
    elif date_filter == 'week':
        week_ago = timezone.now() - timedelta(days=7)
        posts = posts.filter(created_at__gte=week_ago)
    elif date_filter == 'month':
        month_ago = timezone.now() - timedelta(days=30)
        posts = posts.filter(created_at__gte=month_ago)
    
    # Pagination
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories and tags for sidebar
    categories = Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)
    popular_tags = Tag.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0).order_by('-post_count')[:10]
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'popular_tags': popular_tags,
        'search_query': search_query,
        'selected_category': category_slug,
        'selected_tag': tag_slug,
        'selected_date': date_filter,
    }
    return render(request, 'blog_list.html', context)


def blog_detail(request, slug):
    """Blog post detail page"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    # Increment view count (only for non-author visitors)
    if not (request.user.is_authenticated and request.user.is_staff):
        post.increment_views()
    
    # Get related posts
    related_posts = BlogPost.objects.filter(
        is_published=True
    ).exclude(id=post.id).filter(
        Q(category=post.category) | Q(tags__in=post.tags.all())
    ).distinct()[:3]
    
    # Check if user liked this post
    user_liked = False
    if request.session.session_key:
        user_liked = Like.objects.filter(post=post, session_id=request.session.session_key).exists()
    
    # Check if user saved this post
    user_saved = False
    if request.user.is_authenticated:
        user_saved = SavedPost.objects.filter(user=request.user, post=post).exists()
    
    # Get comments (staff can see all, others only approved)
    if request.user.is_authenticated and request.user.is_staff:
        comments = Comment.objects.filter(post=post).order_by('-created_at')
    else:
        comments = Comment.objects.filter(post=post, is_approved=True).order_by('-created_at')
    
    # Comment form
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Your comment has been submitted!')
            return redirect('blog_detail', slug=slug)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'comments': comments,
        'comment_form': comment_form,
        'user_liked': user_liked,
        'user_saved': user_saved,
        'like_count': post.get_like_count(),
    }
    return render(request, 'blog_detail.html', context)


@require_POST
def like_post(request, slug):
    """Like/unlike a post using session ID"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    if not request.session.session_key:
        request.session.create()
    
    session_id = request.session.session_key
    like, created = Like.objects.get_or_create(post=post, session_id=session_id)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'like_count': post.get_like_count()
    })


@login_required
@require_POST
def save_post(request, slug):
    """Save/unsave a post (requires login)"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    saved_post, created = SavedPost.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        saved_post.delete()
        saved = False
    else:
        saved = True
    
    return JsonResponse({
        'saved': saved
    })


@login_required
@require_POST
def delete_comment(request, comment_id):
    """Delete a comment (staff only)"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete comments.')
        return redirect('home')
    
    comment = get_object_or_404(Comment, id=comment_id)
    post_slug = comment.post.slug
    comment.delete()
    messages.success(request, 'Comment deleted successfully.')
    return redirect('blog_detail', slug=post_slug)


def about(request):
    """About/Portfolio page"""
    # Get About page content from database
    about_page = AboutPage.get_instance()
    
    # Get some stats for the about page
    total_posts = BlogPost.objects.filter(is_published=True).count()
    total_views = BlogPost.objects.filter(is_published=True).aggregate(Sum('view_count'))['view_count__sum'] or 0
    total_likes = Like.objects.count()
    
    # Parse topics from text field (one per line)
    topics_list = []
    if about_page.topics:
        topics_list = [topic.strip() for topic in about_page.topics.split('\n') if topic.strip()]
    else:
        # Default topics if none set
        topics_list = [
            'Web Development',
            'Software Engineering',
            'Technology Trends',
            'Personal Projects',
            'Learning Experiences'
        ]
    
    context = {
        'about_page': about_page,
        'total_posts': total_posts,
        'total_views': total_views,
        'total_likes': total_likes,
        'topics_list': topics_list,
    }
    return render(request, 'about.html', context)


def contact(request):
    """Contact page with form - content managed via admin"""
    # Get Contact page content from database
    contact_page = ContactPage.get_instance()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Send email notification (if configured)
            if hasattr(settings, 'CONTACT_EMAIL'):
                try:
                    send_mail(
                        f'New Contact Form: {contact_message.subject}',
                        f'From: {contact_message.name} ({contact_message.email})\n\n{contact_message.message}',
                        settings.DEFAULT_FROM_EMAIL,
                        [settings.CONTACT_EMAIL],
                        fail_silently=True,
                    )
                except Exception:
                    pass
            
            messages.success(request, 'Thank you for your message! I will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'contact_page': contact_page,
    }
    return render(request, 'contact.html', context)


# Author/Admin Views

@login_required
@user_passes_test(is_author)
def dashboard(request):
    """Admin dashboard with analytics"""
    # Get statistics
    total_posts = BlogPost.objects.count()
    published_posts = BlogPost.objects.filter(is_published=True).count()
    draft_posts = BlogPost.objects.filter(is_published=False).count()
    total_views = BlogPost.objects.filter(is_published=True).aggregate(Sum('view_count'))['view_count__sum'] or 0
    total_likes = Like.objects.count()
    total_comments = Comment.objects.count()
    
    # Recent posts
    recent_posts = BlogPost.objects.all().order_by('-created_at')[:5]
    
    # Popular posts
    popular_posts = BlogPost.objects.filter(is_published=True).order_by('-view_count')[:5]
    
    # Monthly stats for chart
    now = timezone.now()
    monthly_stats = []
    for i in range(6):  # Last 6 months
        month_start = now.replace(day=1) - timedelta(days=30 * i)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        month_posts = BlogPost.objects.filter(
            created_at__gte=month_start,
            created_at__lte=month_end
        ).count()
        
        monthly_stats.append({
            'month': month_start.strftime('%b %Y'),
            'count': month_posts
        })
    
    monthly_stats.reverse()
    
    # Posts by status
    posts_by_status = {
        'published': published_posts,
        'drafts': draft_posts,
        'featured': BlogPost.objects.filter(is_featured=True).count(),
    }
    
    context = {
        'total_posts': total_posts,
        'published_posts': published_posts,
        'draft_posts': draft_posts,
        'total_views': total_views,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'recent_posts': recent_posts,
        'popular_posts': popular_posts,
        'monthly_stats': monthly_stats,
        'posts_by_status': posts_by_status,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
@user_passes_test(is_author)
def post_create(request):
    """Create new blog post"""
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save many-to-many relationships (tags)
            messages.success(request, f'Post "{post.title}" created successfully!')
            return redirect('post_edit', id=post.id)
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = BlogPostForm()
    
    return render(request, 'dashboard/post_form.html', {'form': form, 'action': 'Create'})


@login_required
@user_passes_test(is_author)
def post_edit(request, id):
    """Edit existing blog post"""
    post = get_object_or_404(BlogPost, id=id)
    
    # Only allow author to edit their own posts (or superuser)
    if not (post.author == request.user or request.user.is_superuser):
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            # If no new image uploaded, keep the existing one
            if not request.FILES.get('cover_image'):
                post.cover_image = BlogPost.objects.get(id=id).cover_image
            post.save()
            form.save_m2m()
            messages.success(request, f'Post "{post.title}" updated successfully!')
            return redirect('post_edit', id=post.id)
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = BlogPostForm(instance=post)
    
    return render(request, 'dashboard/post_form.html', {'form': form, 'post': post, 'action': 'Edit'})


@login_required
@user_passes_test(is_author)
def post_delete(request, id):
    """Delete blog post"""
    post = get_object_or_404(BlogPost, id=id)
    
    # Only allow author to delete their own posts (or superuser)
    if not (post.author == request.user or request.user.is_superuser):
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        title = post.title
        post.delete()
        messages.success(request, f'Post "{title}" deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'dashboard/post_delete_confirm.html', {'post': post})


@login_required
@user_passes_test(is_author)
def post_list_admin(request):
    """List all posts for admin"""
    posts = BlogPost.objects.all().order_by('-created_at')
    
    # Filter options
    status_filter = request.GET.get('status', '')
    if status_filter == 'published':
        posts = posts.filter(is_published=True)
    elif status_filter == 'draft':
        posts = posts.filter(is_published=False)
    
    search_query = request.GET.get('search', '')
    if search_query:
        posts = posts.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
    
    # Pagination
    paginator = Paginator(posts, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    return render(request, 'dashboard/post_list.html', context)


@login_required
def saved_posts_list(request):
    """List user's saved posts"""
    saved_posts = SavedPost.objects.filter(user=request.user).order_by('-saved_at')
    
    paginator = Paginator(saved_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'dashboard/saved_posts.html', {'page_obj': page_obj})

