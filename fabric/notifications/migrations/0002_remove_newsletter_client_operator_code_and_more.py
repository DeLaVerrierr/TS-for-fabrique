# Generated by Django 4.2.5 on 2023-10-03 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsletter',
            name='client_operator_code',
        ),
        migrations.AddField(
            model_name='newsletter',
            name='clients',
            field=models.ManyToManyField(related_name='newsletters', through='notifications.Message', to='notifications.client'),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone_number',
            field=models.CharField(max_length=11, unique=True),
        ),
    ]