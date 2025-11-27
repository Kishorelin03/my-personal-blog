from django.contrib import admin
from .models import BlogPost, Comment, Like, SavedPost, ContactMessage, Category, Tag, AboutPage, ContactPage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_published', 'is_featured', 'view_count', 'created_at']
    list_filter = ['is_published', 'is_featured', 'category', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'published_at', 'view_count']
    filter_horizontal = ['tags']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'cover_image')
        }),
        ('Metadata', {
            'fields': ('author', 'category', 'tags')
        }),
        ('Status', {
            'fields': ('is_published', 'is_featured')
        }),
        ('Statistics', {
            'fields': ('view_count', 'created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at', 'post']
    search_fields = ['name', 'email', 'text', 'post__title']
    list_editable = ['is_approved']
    actions = ['delete_selected']
    
    def get_queryset(self, request):
        """Show all comments to staff"""
        qs = super().get_queryset(request)
        return qs.select_related('post')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'session_id', 'created_at']
    list_filter = ['created_at']
    search_fields = ['post__title']


@admin.register(SavedPost)
class SavedPostAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'saved_at']
    list_filter = ['saved_at']
    search_fields = ['user__username', 'post__title']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'name', 'updated_at']
    readonly_fields = ['updated_at']
    
    fieldsets = (
        ('Header Information', {
            'fields': ('title', 'subtitle', 'name')
        }),
        ('Profile', {
            'fields': ('profile_image',),
            'description': 'Upload your profile picture here. Recommended size: 300x300px or larger (square images work best).'
        }),
        ('Bio Content', {
            'fields': ('bio',),
            'description': 'Write your main bio/description. This will be displayed on the About page.'
        }),
        ('Topics', {
            'fields': ('topics',),
            'description': 'List the topics you write about, one per line. Each line will appear as a bullet point on the About page.'
        }),
        ('Social Media Links', {
            'fields': ('github_url', 'linkedin_url', 'twitter_url', 'email'),
            'description': 'Add your social media profile URLs. Leave blank if you don\'t want to display a particular link.'
        }),
        ('Metadata', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        return not AboutPage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the only instance
        return False

    def changelist_view(self, request, extra_context=None):
        # Redirect to the single instance if it exists
        if AboutPage.objects.exists():
            obj = AboutPage.objects.get(pk=1)
            from django.shortcuts import redirect
            from django.urls import reverse
            return redirect(reverse('admin:BlogApp_aboutpage_change', args=[obj.pk]))
        return super().changelist_view(request, extra_context)


@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated_at']
    readonly_fields = ['updated_at']
    
    fieldsets = (
        ('Header Information', {
            'fields': ('title', 'subtitle')
        }),
        ('Contact Information', {
            'fields': ('email_label', 'email_value'),
            'description': 'Email contact information displayed on the contact page.'
        }),
        ('GitHub', {
            'fields': ('github_label', 'github_url', 'github_value'),
            'description': 'GitHub profile information. Leave blank if you don\'t want to display GitHub.'
        }),
        ('LinkedIn', {
            'fields': ('linkedin_label', 'linkedin_url', 'linkedin_value'),
            'description': 'LinkedIn profile information. Leave blank if you don\'t want to display LinkedIn.'
        }),
        ('Metadata', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        return not ContactPage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the only instance
        return False

    def changelist_view(self, request, extra_context=None):
        # Redirect to the single instance if it exists
        if ContactPage.objects.exists():
            obj = ContactPage.objects.get(pk=1)
            from django.shortcuts import redirect
            from django.urls import reverse
            return redirect(reverse('admin:BlogApp_contactpage_change', args=[obj.pk]))
        return super().changelist_view(request, extra_context)

