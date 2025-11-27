from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    BlogPostViewSet, CommentViewSet,
    categories_list, tags_list, stats, contact, dashboard_stats,
    login_view, logout_view, current_user, get_csrf_token
)

router = DefaultRouter()
router.register(r'posts', BlogPostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', categories_list, name='api-categories'),
    path('tags/', tags_list, name='api-tags'),
    path('stats/', stats, name='api-stats'),
    path('contact/', contact, name='api-contact'),
    path('dashboard/stats/', dashboard_stats, name='api-dashboard-stats'),
    # Authentication endpoints
    path('auth/csrf/', get_csrf_token, name='api-csrf'),
    path('auth/login/', login_view, name='api-login'),
    path('auth/logout/', logout_view, name='api-logout'),
    path('auth/current-user/', current_user, name='api-current-user'),
]

