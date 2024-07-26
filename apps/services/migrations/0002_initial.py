# Generated by Django 5.0.7 on 2024-07-26 05:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('services', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='payment',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='payment',
            name='price_option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.priceoption'),
        ),
        migrations.AddField(
            model_name='review',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reviewcomment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reviewcomment',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.review'),
        ),
        migrations.AddField(
            model_name='service',
            name='category_detail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.categorydetail'),
        ),
        migrations.AddField(
            model_name='service',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_services', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='service',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='review',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_reviews', to='services.service'),
        ),
        migrations.AddField(
            model_name='priceoption',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.service'),
        ),
        migrations.AddField(
            model_name='order',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='services.service'),
        ),
    ]
