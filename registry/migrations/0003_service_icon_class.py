# Generated by Django 5.1.4 on 2025-01-09 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0002_serviceinfotype_icon_class_alter_service_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='icon_class',
            field=models.CharField(blank=True, help_text='FontAwesome class for an icon representing this Service. E.g., fab fa-google.', max_length=100, null=True),
        ),
    ]
