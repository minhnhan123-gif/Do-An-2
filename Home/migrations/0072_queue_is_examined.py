# Generated by Django 4.2.7 on 2023-12-07 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0071_alter_queue_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='is_examined',
            field=models.BooleanField(default=False),
        ),
    ]
