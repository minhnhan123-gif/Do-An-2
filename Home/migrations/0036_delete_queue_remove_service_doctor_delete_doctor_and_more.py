# Generated by Django 4.2.7 on 2023-11-15 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0035_remove_queue_waiting_time'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Queue',
        ),
        migrations.RemoveField(
            model_name='service',
            name='doctor',
        ),
        migrations.DeleteModel(
            name='Doctor',
        ),
        migrations.DeleteModel(
            name='Service',
        ),
    ]