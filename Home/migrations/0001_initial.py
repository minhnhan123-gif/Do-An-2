# Generated by Django 4.2.7 on 2023-11-06 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ThongTinBenhNhan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('so_CCCD', models.CharField(max_length=15)),
                ('ho_ten', models.CharField(max_length=255)),
                ('ngay_sinh', models.DateField()),
                ('gioi_tinh', models.CharField(max_length=5)),
                ('quoc_tich', models.CharField(max_length=50)),
                ('noi_sinh', models.CharField(max_length=255)),
                ('noi_cu_tru', models.CharField(max_length=255)),
            ],
        ),
    ]
