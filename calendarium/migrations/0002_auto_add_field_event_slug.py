# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.text import slugify
from django.db import models, migrations
import itertools

def slugify_title(apps, schema_editor):  # adding slug based on field 'title'
    Event = apps.get_model("calendarium", "Event")
    for event in Event.objects.all():
        event.slug = orig = slugify(event.title)
        for x in itertools.count(1):
            if not Event.objects.filter(slug=event.slug).exists():
                break
            event.slug = '%s-%d' % (orig, x)
        event.save()


def reverse_slugify(apps, schema_editor):
    pass  # no need to change anything

class Migration(migrations.Migration):

    dependencies = [
        ('calendarium', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.SlugField(default=b'default', max_length=256, verbose_name='Slug'),
            preserve_default=True,
        ),

        migrations.RunPython(slugify_title, reverse_slugify),

        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(default=b'default', unique=True, max_length=256, verbose_name='Slug'),
            preserve_default=True,
        ),
    ]