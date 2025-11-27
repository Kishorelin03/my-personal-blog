from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog_list') + f'?category={self.slug}'


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog_list') + f'?tag={self.slug}'


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField(help_text="Use Markdown or HTML for formatting")
    cover_image = models.ImageField(upload_to='blog_covers/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_published']),
            models.Index(fields=['slug']),
        ]

    def save(self, *args, **kwargs):
        # Only generate slug if it doesn't exist (for new posts)
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure uniqueness
            original_slug = self.slug
            counter = 1
            while BlogPost.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        # Set published_at when first published
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

    def increment_views(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def get_like_count(self):
        return self.likes.count()

    def get_comment_count(self):
        return self.comments.count()


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField(max_length=1000)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"


class Like(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='likes')
    session_id = models.CharField(max_length=40, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['post', 'session_id']
        ordering = ['-created_at']

    def __str__(self):
        return f"Like on {self.post.title} by session {self.session_id[:8]}..."


class SavedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_posts')
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='saved_by_users')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'post']
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.username} saved {self.post.title}"


class ContactPage(models.Model):
    """Model for Contact page content - only one instance should exist"""
    title = models.CharField(max_length=200, default="Get in Touch")
    subtitle = models.TextField(max_length=500, default="I'd love to hear from you. Send me a message and I'll respond as soon as possible.", blank=True)
    email_label = models.CharField(max_length=100, default="Email", blank=True)
    email_value = models.EmailField(blank=True, null=True)
    github_label = models.CharField(max_length=100, default="GitHub", blank=True)
    github_url = models.URLField(blank=True, null=True)
    github_value = models.CharField(max_length=200, blank=True, null=True, help_text="Display text for GitHub (e.g., github.com/username)")
    linkedin_label = models.CharField(max_length=100, default="LinkedIn", blank=True)
    linkedin_url = models.URLField(blank=True, null=True)
    linkedin_value = models.CharField(max_length=200, blank=True, null=True, help_text="Display text for LinkedIn (e.g., linkedin.com/in/username)")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contact Page"
        verbose_name_plural = "Contact Page"

    def __str__(self):
        return "Contact Page Content"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        """Get or create the single Contact page instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=2000)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class AboutPage(models.Model):
    """Model for About page content - only one instance should exist"""
    title = models.CharField(max_length=200, default="About Me")
    subtitle = models.CharField(max_length=300, default="Welcome to my personal blog", blank=True)
    name = models.CharField(max_length=100, default="Kishorelin")
    bio = models.TextField(
        help_text="Main bio/description text",
        default="This is my personal blog where I share my thoughts, experiences, projects, and knowledge on various topics that interest me.\n\nI'm passionate about technology, programming, and continuous learning. Through this blog, I aim to document my journey, share what I've learned, and connect with like-minded individuals.",
        blank=True
    )
    profile_image = models.ImageField(upload_to='about/', blank=True, null=True)
    topics = models.TextField(
        help_text="List of topics you write about (one per line)",
        default="Web Development\nSoftware Engineering\nTechnology Trends\nPersonal Projects\nLearning Experiences",
        blank=True
    )
    github_url = models.URLField(blank=True, null=True, help_text="Your GitHub profile URL")
    linkedin_url = models.URLField(blank=True, null=True, help_text="Your LinkedIn profile URL")
    twitter_url = models.URLField(blank=True, null=True, help_text="Your Twitter/X profile URL")
    email = models.EmailField(blank=True, null=True, help_text="Your contact email")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"

    def __str__(self):
        return "About Page Content"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        """Get or create the single About page instance"""
        obj, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'title': 'About Me',
                'subtitle': 'Welcome to my personal blog',
                'name': 'Kishorelin',
                'bio': 'This is my personal blog where I share my thoughts, experiences, projects, and knowledge on various topics that interest me.\n\nI\'m passionate about technology, programming, and continuous learning. Through this blog, I aim to document my journey, share what I\'ve learned, and connect with like-minded individuals.',
                'topics': 'Web Development\nSoftware Engineering\nTechnology Trends\nPersonal Projects\nLearning Experiences'
            }
        )
        return obj

