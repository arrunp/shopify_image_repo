# Generated by Django 3.1.4 on 2021-01-01 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0005_auto_20210101_0259'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='imageName',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
