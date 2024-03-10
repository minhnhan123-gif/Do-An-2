# Generated by Django 4.2.7 on 2023-11-16 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0041_remove_queue_id_alter_queue_queue_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='queue',
            name='queue_number',
            field=models.IntegerField(default=0),
        ),
    ]