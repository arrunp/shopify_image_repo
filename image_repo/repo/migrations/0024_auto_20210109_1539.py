# Generated by Django 3.1.4 on 2021-01-09 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0023_auto_20210109_0309'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='title',
            field=models.CharField(default='sample', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='history',
            name='url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='history',
            name='action',
            field=models.CharField(choices=[('uploaded', 'uploaded'), ('deleted', 'deleted')], max_length=8),
        ),
    ]
