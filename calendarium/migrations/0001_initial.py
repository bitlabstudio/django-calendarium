# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations

import filer.fields.image
import calendarium.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('filer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField(verbose_name='Start date')),
                ('end', models.DateTimeField(verbose_name='End date')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('description', models.TextField(max_length=2048, verbose_name='Description', blank=True)),
                ('end_recurring_period', models.DateTimeField(null=True, verbose_name='End of recurring', blank=True)),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('slug', models.SlugField(max_length=256, verbose_name='Slug', blank=True)),
                ('color', calendarium.models.ColorField(max_length=6, verbose_name='Color')),
                ('parent', models.ForeignKey(related_name='parents', verbose_name='Parent', blank=True, to='calendarium.EventCategory', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField()),
                ('relation_type', models.CharField(max_length=32, null=True, verbose_name='Relation type', blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('event', models.ForeignKey(verbose_name='Event', to='calendarium.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Occurrence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField(verbose_name='Start date')),
                ('end', models.DateTimeField(verbose_name='End date')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('description', models.TextField(max_length=2048, verbose_name='Description', blank=True)),
                ('original_start', models.DateTimeField(verbose_name='Original start')),
                ('original_end', models.DateTimeField(verbose_name='Original end')),
                ('cancelled', models.BooleanField(default=False, verbose_name='Cancelled')),
                ('title', models.CharField(max_length=256, verbose_name='Title', blank=True)),
                ('created_by', models.ForeignKey(related_name='occurrences', verbose_name='Created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('event', models.ForeignKey(related_name='occurrences', verbose_name='Event', to='calendarium.Event')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
                ('frequency', models.CharField(max_length=10, verbose_name='frequency', choices=[('YEARLY', 'Yearly'), ('MONTHLY', 'Monthly'), ('WEEKLY', 'Weekly'), ('DAILY', 'Daily')])),
                ('params', models.TextField(null=True, verbose_name='params', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='category',
            field=models.ForeignKey(related_name='events', verbose_name='Category', blank=True, to='calendarium.EventCategory', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='created_by',
            field=models.ForeignKey(related_name='events', verbose_name='Created by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='image',
            field=filer.fields.image.FilerImageField(related_name='calendarium_event_images', verbose_name='Image', blank=True, to='filer.Image', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='rule',
            field=models.ForeignKey(verbose_name='Rule', blank=True, to='calendarium.Rule', null=True),
        ),
    ]
