# Generated by Django 4.2.7 on 2023-12-06 08:15

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0067_alter_queue_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queue',
            name='doctor',
            field=models.CharField(max_length=100),  # Chỉnh kiểu của trường thành CharField
        ),
        migrations.AlterField(
            model_name='queue',
            name='service',
            field=models.CharField(max_length=100),  # Chỉnh kiểu của trường thành CharField
        ),
    ]
