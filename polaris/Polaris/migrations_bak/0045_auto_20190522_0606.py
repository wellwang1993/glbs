# Generated by Django 2.1.2 on 2019-05-22 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Polaris', '0044_auto_20190522_0531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tb_fact_adminip_info',
            name='admin_ip',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
