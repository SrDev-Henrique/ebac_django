from django.db import migrations, models
from django.utils.text import slugify


def populate_slugs(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    for post in Post.objects.all():
        base_slug = slugify(post.title) or f"post-{post.pk}"
        slug = base_slug
        counter = 1
        while Post.objects.filter(slug=slug).exclude(pk=post.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        post.slug = slug
        post.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="created_at",
            new_name="created_on",
        ),
        migrations.AddField(
            model_name="post",
            name="slug",
            field=models.SlugField(blank=True, max_length=200, null=True),
        ),
        migrations.RunPython(populate_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="post",
            name="slug",
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]
