# Generated by Django 4.2.5 on 2023-10-03 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_newsletter_client_tag_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='client_tag',
            field=models.CharField(default='new', max_length=50),
        ),
    ]