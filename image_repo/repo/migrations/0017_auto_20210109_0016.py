# Generated by Django 3.1.4 on 2021-01-09 05:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('repo', '0016_auto_20210109_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='uploader',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
