# Generated by Django 5.0.7 on 2024-07-23 00:07

import shortuuid.django_fields
import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=22, max_length=128, prefix='', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('htmlcontent', tinymce.models.HTMLField(default='')),
                ('price', models.IntegerField()),
                ('portfolio_start', models.DateTimeField()),
                ('portfolio_end', models.DateTimeField()),
                ('show', models.IntegerField(default=0)),
                ('like', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PortfolioEditor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('htmlcontent', tinymce.models.HTMLField()),
            ],
        ),
        migrations.CreateModel(
            name='PortfolioImage',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=22, max_length=128, prefix='', primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='portfolio_images')),
            ],
        ),
        migrations.CreateModel(
            name='PortfolioVideo',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=22, max_length=128, prefix='', primary_key=True, serialize=False)),
                ('video', models.FileField(upload_to='portfolio_videos')),
            ],
        ),
    ]
