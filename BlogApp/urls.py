from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Public URLs
    path('', views.home, name='home'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('blog/<slug:slug>/like/', views.like_post, name='like_post'),
    path('blog/<slug:slug>/save/', views.save_post, name='save_post'),
    path('about/', views.about, name='about'),
    # path('contact/', views.contact, name='contact'),  # Removed per user request
    
    # Admin/Dashboard URLs (require staff login)
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/posts/', views.post_list_admin, name='post_list_admin'),
    path('dashboard/new/', views.post_create, name='post_create'),
    path('dashboard/edit/<int:id>/', views.post_edit, name='post_edit'),
    path('dashboard/delete/<int:id>/', views.post_delete, name='post_delete'),
    path('dashboard/saved/', views.saved_posts_list, name='saved_posts_list'),
    
    # Comment management (staff only)
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]

