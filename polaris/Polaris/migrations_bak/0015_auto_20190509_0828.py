# Generated by Django 2.1.2 on 2019-05-09 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Polaris', '0014_auto_20190509_0822'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tb_fact_temp_view_info',
            name='view_type',
        ),
        migrations.DeleteModel(
            name='tb_fact_temp_view_info',
        ),
    ]
