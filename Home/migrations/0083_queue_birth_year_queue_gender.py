# Generated by Django 4.2.7 on 2024-01-13 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0082_alter_thongtinbenhnhan_gioi_tinh_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='birth_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='queue',
            name='gender',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]