# Generated by Django 4.1.5 on 2023-01-28 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Name")),
                (
                    "photo",
                    models.ImageField(upload_to="Blog/%Y/%m/%d/", verbose_name="Image"),
                ),
                ("description", models.TextField(verbose_name="Description")),
                ("active", models.BooleanField(default=True, verbose_name="Active")),
                (
                    "timestamp",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True,
                        editable=False,
                        max_length=255,
                        null=True,
                        verbose_name="Slug",
                    ),
                ),
            ],
            options={
                "ordering": ("-timestamp",),
            },
        ),
        migrations.CreateModel(
            name="BlogCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, unique=True, verbose_name="Name"),
                ),
                ("active", models.BooleanField(default=True, verbose_name="Active")),
                (
                    "timestamp",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True,
                        editable=False,
                        max_length=255,
                        null=True,
                        verbose_name="Slug",
                    ),
                ),
            ],
            options={
                "ordering": ("-timestamp",),
            },
        ),
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=255, verbose_name="First Name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=255, verbose_name="Last Name"),
                ),
                ("email", models.EmailField(max_length=255, verbose_name="Email")),
                ("subject", models.CharField(max_length=255, verbose_name="Subject")),
                ("phone", models.CharField(max_length=255, verbose_name="Phone")),
                ("message", models.TextField(verbose_name="Message")),
                ("active", models.BooleanField(default=True, verbose_name="Active")),
                (
                    "timestamp",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
            ],
            options={
                "ordering": ("-timestamp",),
            },
        ),
        migrations.CreateModel(
            name="Subscriber",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=255, unique=True, verbose_name="Email"
                    ),
                ),
                ("active", models.BooleanField(default=True, verbose_name="Active")),
                (
                    "timestamp",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
            ],
            options={
                "ordering": ("-timestamp",),
            },
        ),
        migrations.CreateModel(
            name="Testimony",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "full_name",
                    models.CharField(max_length=255, verbose_name="Full Name"),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="Testimony/%Y/%m/",
                        verbose_name="Image",
                    ),
                ),
                (
                    "occupation",
                    models.CharField(max_length=255, verbose_name="Occupation"),
                ),
                ("description", models.TextField(verbose_name="Description")),
                ("active", models.BooleanField(default=True, verbose_name="Status")),
                (
                    "timestamp",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
            ],
            options={
                "verbose_name_plural": "Testimonies",
                "ordering": ("-timestamp",),
            },
        ),
        migrations.CreateModel(
            name="BlogComment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Name")),
                ("email", models.EmailField(max_length=255, verbose_name="Email")),
                (
                    "website",
                    models.URLField(
                        blank=True, max_length=255, null=True, verbose_name="Website"
                    ),
                ),
                ("comment", models.TextField(verbose_name="Comment")),
                ("active", models.BooleanField(default=True, verbose_name="Active")),
                (
                    "timestamp",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
                (
                    "blog",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comment_blog",
                        to="landing_app.blog",
                    ),
                ),
            ],
            options={
                "ordering": ("-timestamp",),
            },
        ),
        migrations.AddField(
            model_name="blog",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="blog_category",
                to="landing_app.blogcategory",
            ),
        ),
    ]