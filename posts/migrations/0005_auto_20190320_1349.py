# Generated by Django 2.1.7 on 2019-03-20 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_like_like'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='like',
            new_name='is_liked',
        ),
    ]
