# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-06 22:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0020_auto_20170628_1136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dependenttier',
            name='utterance',
        ),
        migrations.AddField(
            model_name='token',
            name='speaker_sex',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='token',
            name='target_child',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='all_related_tokens', to='db.Participant'),
        ),
        migrations.AddField(
            model_name='token',
            name='target_child_age',
            field=models.FloatField(blank=True, db_index=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='token',
            name='target_child_name',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='token',
            name='target_child_sex',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='transcript',
            name='target_child_name',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='utterance',
            name='speaker_sex',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='utterance',
            name='target_child',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='all_related_utterances', to='db.Participant'),
        ),
        migrations.AddField(
            model_name='utterance',
            name='target_child_age',
            field=models.FloatField(blank=True, db_index=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='utterance',
            name='target_child_name',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='utterance',
            name='target_child_sex',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='DependentTier',
        ),
    ]
