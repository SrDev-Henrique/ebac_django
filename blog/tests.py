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
            status=1,
        )

    def test_post_is_persisted(self):
        self.assertEqual(Post.objects.count(), 1)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    def test_post_fields(self):
        post = Post.objects.get(pk=self.post.pk)
        self.assertEqual(post.title, "Primeiro post")
        self.assertEqual(post.content, "Conteúdo do post de teste")
        self.assertEqual(post.author, "Henrique")
        self.assertEqual(post.slug, "primeiro-post")
        self.assertEqual(post.status, 1)

    def test_created_on_is_auto_filled(self):
        self.assertIsNotNone(self.post.created_on)
        self.assertLessEqual(self.post.created_on, timezone.now())

    def test_default_status_is_draft(self):
        draft = Post.objects.create(
            title="Rascunho",
            content="Ainda não publicado",
            author="Henrique",
        )
        self.assertEqual(draft.status, 0)
        self.assertEqual(draft.get_status_display(), "Draft")

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
            ("title", "slug", "status", "created_on"),
        )

    def test_post_admin_prepopulated_fields(self):
        self.assertEqual(PostAdmin.prepopulated_fields, {"slug": ("title",)})

    def test_post_admin_list_filter(self):
        self.assertEqual(PostAdmin.list_filter, ("status",))

    def test_admin_post_changelist_is_accessible(self):
        user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123",
        )
        self.client.force_login(user)
        response = self.client.get(reverse("admin:blog_post_changelist"))
        self.assertEqual(response.status_code, 200)

    def test_admin_add_post_form_includes_slug_and_status(self):
        user = get_user_model().objects.create_superuser(
            username="admin2",
            email="admin2@example.com",
            password="admin123",
        )
        self.client.force_login(user)
        response = self.client.get(reverse("admin:blog_post_add"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="slug"')
        self.assertContains(response, 'name="status"')
        self.assertContains(response, "Draft")
        self.assertContains(response, "Publish")
