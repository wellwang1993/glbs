# Generated by Django 2.1.2 on 2019-05-14 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Polaris', '0031_tb_fact_dnszone_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tb_fact_view_info',
            name='view_type',
        ),
        migrations.DeleteModel(
            name='tb_fact_view_info',
        ),
    ]
