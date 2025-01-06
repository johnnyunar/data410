# Generated by Django 5.1.4 on 2025-01-06 15:46

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Service",
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
                    "uuid",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        unique=True,
                        verbose_name="UUID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "name",
                    models.CharField(
                        help_text="Name of the third-party service.",
                        max_length=255,
                        unique=True,
                    ),
                ),
                (
                    "website",
                    models.URLField(
                        blank=True,
                        help_text="Official website of the service.",
                        null=True,
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="Logo or image representing the service.",
                        null=True,
                        upload_to="",
                    ),
                ),
                (
                    "rating",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Average rating of the service.",
                        max_digits=3,
                        null=True,
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Unique URL path to access this service.",
                        max_length=255,
                        unique=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Service",
                "verbose_name_plural": "Services",
            },
        ),
        migrations.CreateModel(
            name="ServiceInfoCategory",
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
                    "uuid",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        unique=True,
                        verbose_name="UUID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "name",
                    models.CharField(
                        help_text="Name of the service info category, e.g., Privacy, Security, AI.",
                        max_length=255,
                        unique=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Service Info Category",
                "verbose_name_plural": "Service Info Categories",
                "ordering": ["order"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ServiceInfoType",
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
                    "uuid",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        unique=True,
                        verbose_name="UUID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "name",
                    models.CharField(
                        help_text="Name of the service info type, e.g., What to be aware of, How to delete data.",
                        max_length=255,
                        unique=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Service Info Type",
                "verbose_name_plural": "Service Info Types",
            },
        ),
        migrations.CreateModel(
            name="ServiceInfo",
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
                    "uuid",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        unique=True,
                        verbose_name="UUID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="Description of the service.", null=True
                    ),
                ),
                (
                    "service",
                    models.ForeignKey(
                        help_text="The third-party service associated with this info.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="service_infos",
                        to="registry.service",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        help_text="Category of service info.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="service_infos",
                        to="registry.serviceinfocategory",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        help_text="Type of service info.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="service_infos",
                        to="registry.serviceinfotype",
                    ),
                ),
            ],
            options={
                "verbose_name": "Service Info",
                "verbose_name_plural": "Service Infos",
            },
        ),
        migrations.CreateModel(
            name="ServiceInfoPoint",
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
                    "uuid",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        unique=True,
                        verbose_name="UUID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "text",
                    models.CharField(
                        help_text="A point of information about the service.",
                        max_length=255,
                    ),
                ),
                (
                    "service_info",
                    models.ForeignKey(
                        help_text="The service info associated with this point.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="points",
                        to="registry.serviceinfo",
                    ),
                ),
            ],
            options={
                "verbose_name": "Service Info Point",
                "verbose_name_plural": "Service Info Points",
            },
        ),
        migrations.CreateModel(
            name="ServiceURL",
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
                    "uuid",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        unique=True,
                        verbose_name="UUID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "url_type",
                    models.CharField(
                        help_text="Type or purpose of the URL (e.g., API docs, support page, privacy policy, data removal page).",
                        max_length=100,
                    ),
                ),
                ("url", models.URLField()),
                (
                    "service",
                    models.ForeignKey(
                        help_text="The third-party service associated with this URL.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="urls",
                        to="registry.service",
                    ),
                ),
            ],
            options={
                "verbose_name": "Service URL",
                "verbose_name_plural": "Service URLs",
            },
        ),
    ]
