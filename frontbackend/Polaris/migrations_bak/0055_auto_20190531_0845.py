# Generated by Django 2.1.2 on 2019-05-31 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Polaris', '0054_tb_fact_device_info_node_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tb_dimension_nameid_view_info',
            name='nameid_status',
            field=models.CharField(choices=[('enable', 'enable'), ('disable', 'disable')], default='enable', max_length=256),
        ),
    ]