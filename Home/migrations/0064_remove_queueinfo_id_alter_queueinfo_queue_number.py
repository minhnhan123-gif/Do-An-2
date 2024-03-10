from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0063_queueinfo_delete_queue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='queueinfo',
            name='queue_number',
        ),
    ]