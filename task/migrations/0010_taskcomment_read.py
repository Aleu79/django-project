# Generated by Django 5.1.4 on 2024-12-18 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0009_tasknotification'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskcomment',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
