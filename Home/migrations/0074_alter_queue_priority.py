# Generated by Django 4.2.7 on 2023-12-07 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0073_queue_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queue',
            name='priority',
            field=models.BooleanField(default=False),
        ),
    ]