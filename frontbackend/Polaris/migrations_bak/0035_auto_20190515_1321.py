# Generated by Django 2.1.2 on 2019-05-15 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Polaris', '0034_auto_20190515_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tb_dimension_nameid_view_device_info',
            name='nameid_device_status',
            field=models.CharField(choices=[('enable', 'enable'), ('disable', 'disable')], max_length=256),
        ),
    ]
