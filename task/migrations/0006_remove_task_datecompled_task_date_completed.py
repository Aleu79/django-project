# Generated by Django 5.1.4 on 2024-12-17 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0005_remove_taskcategory_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='datecompled',
        ),
        migrations.AddField(
            model_name='task',
            name='date_completed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
