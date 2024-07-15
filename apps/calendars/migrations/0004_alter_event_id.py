# Generated by Django 5.0.6 on 2024-07-15 04:51

import shortuuid.django_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendars', '0003_alter_event_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='id',
            field=shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=22, max_length=128, prefix='', primary_key=True, serialize=False),
        ),
    ]
