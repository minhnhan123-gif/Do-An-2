# Generated by Django 4.2.7 on 2023-11-12 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0011_alter_thongtinbenhnhan_so'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thongtinbenhnhan',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
