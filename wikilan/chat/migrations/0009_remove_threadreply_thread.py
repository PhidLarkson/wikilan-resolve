# Generated by Django 4.2.8 on 2024-04-12 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_threadreply_key_alter_threadreply_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='threadreply',
            name='thread',
        ),
    ]
