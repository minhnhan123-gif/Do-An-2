# Generated by Django 4.2.7 on 2023-11-16 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0053_queue'),
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
