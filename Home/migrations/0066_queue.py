# Generated by Django 4.2.7 on 2023-11-16 13:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0065_delete_queueinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regis_time', models.DateTimeField(auto_now_add=True)),
                ('queue_number', models.IntegerField(default=0)),
                ('patient', models.CharField(max_length=100)),
                ('service', models.CharField(max_length=100)),
                ('doctor', models.CharField(max_length=100)),
                ('registration_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]