from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count, Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator

from .models import BlogPost, Comment, Like, SavedPost, Category, Tag, ContactMessage
from .serializers import (
    BlogPostListSerializer, BlogPostDetailSerializer,
    CommentSerializer, CommentCreateSerializer,
    LikeSerializer, SavedPostSerializer,
    CategorySerializer, TagSerializer, ContactMessageSerializer
)


class BlogPostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing blog posts
    """
    queryset = BlogPost.objects.filter(is_published=True).select_related(
        'author', 'category'
    ).prefetch_related('tags').order_by('-created_at')
    pagination_class = BlogPostPagination
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BlogPostDetailSerializer
        return BlogPostListSerializer

    def get_queryset(self):
        queryset = self.queryset

        # Search
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(tags__name__icontains=search)
            ).distinct()

        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)

        # Filter by tag
        tag = self.request.query_params.get('tag', None)
        if tag:
            queryset = queryset.filter(tags__slug=tag)

        # Filter by date
        date_filter = self.request.query_params.get('date', None)
        if date_filter == 'today':
            queryset = queryset.filter(created_at__date=timezone.now().date())
        elif date_filter == 'week':
            week_ago = timezone.now() - timedelta(days=7)
            queryset = queryset.filter(created_at__gte=week_ago)
        elif date_filter == 'month':
            month_ago = timezone.now() - timedelta(days=30)
            queryset = queryset.filter(created_at__gte=month_ago)

        # Featured posts
        featured = self.request.query_params.get('featured', None)
        if featured == 'true':
            queryset = queryset.filter(is_featured=True)

        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        if not (request.user.is_authenticated and request.user.is_staff):
            instance.increment_views()
        
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def like(self, request, slug=None):
        """Like or unlike a post"""
        post = self.get_object()

        if not request.session.session_key:
            request.session.create()

        session_id = request.session.session_key
        like, created = Like.objects.get_or_create(post=post, session_id=session_id)

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        return Response({
            'liked': liked,
            'like_count': post.get_like_count()
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def save(self, request, slug=None):
        """Save or unsave a post"""
        post = self.get_object()
        saved_post, created = SavedPost.objects.get_or_create(
            user=request.user,
            post=post
        )

        if not created:
            saved_post.delete()
            saved = False
        else:
            saved = True

        return Response({'saved': saved})


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for comments
    """
    queryset = Comment.objects.filter(is_approved=True).order_by('-created_at')
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer

    def get_queryset(self):
        queryset = self.queryset
        post_id = self.request.query_params.get('post', None)
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(is_approved=True)
        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def categories_list(request):
    """Get all categories with post counts"""
    categories = Category.objects.annotate(
        post_count=Count('posts', filter=Q(posts__is_published=True))
    ).filter(post_count__gt=0)
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def tags_list(request):
    """Get all tags with post counts"""
    tags = Tag.objects.annotate(
        post_count=Count('posts', filter=Q(posts__is_published=True))
    ).filter(post_count__gt=0).order_by('-post_count')[:20]
    serializer = TagSerializer(tags, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def stats(request):
    """Get blog statistics"""
    total_posts = BlogPost.objects.filter(is_published=True).count()
    total_views = BlogPost.objects.filter(is_published=True).aggregate(
        Sum('view_count')
    )['view_count__sum'] or 0
    total_likes = Like.objects.count()
    total_comments = Comment.objects.filter(is_approved=True).count()

    return Response({
        'total_posts': total_posts,
        'total_views': total_views,
        'total_likes': total_likes,
        'total_comments': total_comments,
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def contact(request):
    """Submit contact form"""
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Admin views for dashboard
# CSRF token endpoint
@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    """Get CSRF token for authentication"""
    return Response({'csrfToken': get_token(request)})


# Authentication views
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Login endpoint for API"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        if user.is_active:
            login(request, user)
            return Response({
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email or '',
                    'first_name': user.first_name or '',
                    'last_name': user.last_name or '',
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser,
                }
            })
        else:
            return Response(
                {'error': 'Account is disabled'},
                status=status.HTTP_403_FORBIDDEN
            )
    else:
        return Response(
            {'error': 'Invalid username or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Logout endpoint"""
    logout(request)
    return Response({'success': True})


@api_view(['GET'])
@permission_classes([AllowAny])
def current_user(request):
    """Get current authenticated user"""
    if request.user.is_authenticated:
        return Response({
            'authenticated': True,
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'is_staff': request.user.is_staff,
                'is_superuser': request.user.is_superuser,
            }
        })
    else:
        return Response({
            'authenticated': False,
            'user': None
        })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def dashboard_stats(request):
    """Get dashboard statistics for admin"""
    total_posts = BlogPost.objects.count()
    published_posts = BlogPost.objects.filter(is_published=True).count()
    draft_posts = BlogPost.objects.filter(is_published=False).count()
    total_views = BlogPost.objects.filter(is_published=True).aggregate(
        Sum('view_count')
    )['view_count__sum'] or 0
    total_likes = Like.objects.count()
    total_comments = Comment.objects.count()

    # Monthly stats
    now = timezone.now()
    monthly_stats = []
    for i in range(6):
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

    return Response({
        'total_posts': total_posts,
        'published_posts': published_posts,
        'draft_posts': draft_posts,
        'total_views': total_views,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'monthly_stats': monthly_stats,
        'posts_by_status': {
            'published': published_posts,
            'drafts': draft_posts,
            'featured': BlogPost.objects.filter(is_featured=True).count(),
        }
    })

