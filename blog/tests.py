from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .admin import PostAdmin
from .models import Post


class PostModelTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title="Primeiro post",
            content="Conteúdo do post de teste",
            author="Henrique",
        )

    def test_post_is_persisted(self):
        self.assertEqual(Post.objects.count(), 1)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    def test_post_fields(self):
        post = Post.objects.get(pk=self.post.pk)
        self.assertEqual(post.title, "Primeiro post")
        self.assertEqual(post.content, "Conteúdo do post de teste")
        self.assertEqual(post.author, "Henrique")

    def test_created_at_is_auto_filled(self):
        self.assertIsNotNone(self.post.created_at)
        self.assertLessEqual(self.post.created_at, timezone.now())

    def test_str_returns_title(self):
        self.assertEqual(str(self.post), "Primeiro post")


class PostViewTest(TestCase):
    def test_home_returns_hello_world(self):
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Hello World")

    def test_home_url_name_resolves(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Hello World")


class PostAdminTest(TestCase):
    def test_post_is_registered_in_admin(self):
        self.assertIn(Post, admin.site._registry)
        self.assertIsInstance(admin.site._registry[Post], PostAdmin)

    def test_post_admin_list_display(self):
        self.assertEqual(
            PostAdmin.list_display,
            ("title", "author", "created_at"),
        )

    def test_admin_post_changelist_is_accessible(self):
        user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123",
        )
        self.client.force_login(user)
        response = self.client.get(reverse("admin:blog_post_changelist"))
        self.assertEqual(response.status_code, 200)
