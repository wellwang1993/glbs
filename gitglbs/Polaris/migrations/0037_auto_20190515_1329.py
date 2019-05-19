# Generated by Django 2.1.2 on 2019-05-15 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Polaris', '0036_auto_20190515_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tb_fact_device_info',
            name='vip_enable_switch',
            field=models.CharField(choices=[('enable', 'enable'), ('disable', 'disable')], default='enable', max_length=256),
        ),
        migrations.AlterField(
            model_name='tb_fact_device_info',
            name='vip_status',
            field=models.CharField(choices=[('enable', 'enable'), ('disable', 'disable')], max_length=256),
        ),
    ]
