# Generated by Django 5.1.4 on 2025-01-02 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("registry", "0003_serviceinfocategory_order"),
    ]

    operations = [
        migrations.AlterField(
            model_name="serviceinfocategory",
            name="order",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
