# Generated by Django 4.2.5 on 2023-10-03 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_alter_newsletter_client_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsletter',
            name='clients',
        ),
    ]
