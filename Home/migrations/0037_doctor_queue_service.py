# Generated by Django 4.2.7 on 2023-11-15 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0036_delete_queue_remove_service_doctor_delete_doctor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regis_time', models.DateTimeField(auto_now_add=True)),
                ('queue_number', models.IntegerField(default=0)),
                ('patient', models.CharField(max_length=100)),
                ('service', models.CharField(max_length=100)),
                ('doctor', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='Home.doctor')),
            ],
        ),
    ]
