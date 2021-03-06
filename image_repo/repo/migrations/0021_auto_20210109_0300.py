# Generated by Django 3.1.4 on 2021-01-09 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0020_auto_20210109_0027'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('action', models.CharField(choices=[('uploaded', 'Unpublished'), ('deleted', 'Published')], max_length=8)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='image',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
