# Generated by Django 4.2.8 on 2024-04-12 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_messagethread_session_reply_to_threadreply'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagethread',
            name='content',
            field=models.TextField(default='', max_length=50),
        ),
    ]
