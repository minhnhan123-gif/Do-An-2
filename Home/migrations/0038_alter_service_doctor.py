# Generated by Django 4.2.7 on 2023-11-15 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0037_doctor_queue_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Home.doctor'),
        ),
    ]