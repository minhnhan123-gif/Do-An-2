# Generated by Django 4.2.7 on 2023-11-12 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0018_thongtinbenhnhan_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thongtinbenhnhan',
            name='user',
        ),
    ]