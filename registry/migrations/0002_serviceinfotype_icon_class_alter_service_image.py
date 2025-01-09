# Generated by Django 5.1.4 on 2025-01-09 10:12

import core.utils
import functools
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceinfotype',
            name='icon_class',
            field=models.CharField(blank=True, help_text='FontAwesome class for an icon representing this type. E.g., fas fa-lock.', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='image',
            field=models.ImageField(blank=True, help_text='Logo or image representing the service.', null=True, upload_to=functools.partial(core.utils.generate_random_filename, *(), **{'subdir': 'services/images/'})),
        ),
    ]
