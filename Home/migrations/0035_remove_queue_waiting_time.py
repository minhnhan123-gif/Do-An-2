# Generated by Django 4.2.7 on 2023-11-15 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0034_alter_queue_doctor_alter_queue_patient_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='queue',
            name='waiting_time',
        ),
    ]
