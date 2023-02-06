# Generated by Django 4.1.5 on 2023-02-06 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("landing_app", "0010_alter_product_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Doctor",
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
                    "emp_no",
                    models.CharField(
                        blank=True,
                        max_length=30,
                        null=True,
                        unique=True,
                        verbose_name="Numero de Service(Travail)",
                    ),
                ),
                (
                    "age",
                    models.IntegerField(
                        blank=True, default="0", null=True, verbose_name="Age"
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("Masculin", "Masculin"), ("Feminin", "Feminin")],
                        max_length=100,
                        null=True,
                        verbose_name="Options",
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Numéro de téléphone",
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Address Patient",
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="Images/%Y/%m/",
                        verbose_name="Photo",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Date de Creation"
                    ),
                ),
                ("active", models.BooleanField(default=True, verbose_name="Est actif")),
                (
                    "timestamp",
                    models.DateTimeField(auto_now_add=True, verbose_name="Créé le"),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, verbose_name="Modifié le"),
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
            options={"ordering": ("-timestamp",),},
        ),
        migrations.CreateModel(
            name="Pharmacy",
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
                ("name", models.CharField(max_length=255, verbose_name="Nom Pharmacy")),
                (
                    "location",
                    models.CharField(max_length=255, verbose_name="Localisation"),
                ),
                ("address", models.TextField(verbose_name="Address")),
                ("specialization", models.TextField(verbose_name="Specialisation")),
                ("start_hour", models.TimeField(verbose_name="Heure d'ouverture")),
                ("end_hour", models.TimeField(verbose_name="Heure de fermeture")),
                ("start_day", models.DateField(verbose_name="Jour Ouvrable")),
                ("end_day", models.DateField(verbose_name="Jour de fermeture")),
                ("active", models.BooleanField(default=True, verbose_name="Est actif")),
                (
                    "timestamp",
                    models.DateTimeField(auto_now_add=True, verbose_name="Créé le"),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, verbose_name="Modifié le"),
                ),
            ],
            options={"ordering": ("-timestamp",),},
        ),
    ]