from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from .models import BlogPost, Category, Tag, Comment, Like, SavedPost, ContactMessage


class BlogPostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.category = Category.objects.create(name='Technology')
        self.tag = Tag.objects.create(name='Python')

    def test_post_creation(self):
        post = BlogPost.objects.create(
            title='Test Post',
            content='This is a test post',
            author=self.user,
            category=self.category,
            is_published=True
        )
        post.tags.add(self.tag)
        
        self.assertEqual(str(post), 'Test Post')
        self.assertEqual(post.slug, 'test-post')
        self.assertTrue(post.is_published)

    def test_post_slug_uniqueness(self):
        post1 = BlogPost.objects.create(
            title='Test Post',
            content='Content 1',
            author=self.user
        )
        post2 = BlogPost.objects.create(
            title='Test Post',
            content='Content 2',
            author=self.user
        )
        
        self.assertNotEqual(post1.slug, post2.slug)
        self.assertTrue(post2.slug.startswith('test-post-'))


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.post = BlogPost.objects.create(
            title='Test Post',
            content='Content',
            author=self.user,
            is_published=True
        )

    def test_comment_creation(self):
        comment = Comment.objects.create(
            post=self.post,
            name='John Doe',
            email='john@example.com',
            text='Great post!'
        )
        
        self.assertEqual(str(comment), f'Comment by John Doe on Test Post')
        self.assertTrue(comment.is_approved)


class LikeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.post = BlogPost.objects.create(
            title='Test Post',
            content='Content',
            author=self.user,
            is_published=True
        )

    def test_like_creation(self):
        like = Like.objects.create(
            post=self.post,
            session_id='test_session_123'
        )
        
        self.assertEqual(like.post, self.post)
        self.assertEqual(like.session_id, 'test_session_123')

