# Generated by Django 2.1.2 on 2019-05-10 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Polaris', '0020_auto_20190510_0633'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tb_dimension_nameid_view_device_info_test',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='tb_dimension_nameid_view_device_info_test',
            name='nameid_device_id',
        ),
        migrations.RemoveField(
            model_name='tb_dimension_nameid_view_device_info_test',
            name='nameid_id',
        ),
        migrations.RemoveField(
            model_name='tb_dimension_nameid_view_device_info_test',
            name='nameid_view_id',
        ),
        migrations.AlterUniqueTogether(
            name='tb_dimension_nameid_view_info_test',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='tb_dimension_nameid_view_info_test',
            name='nameid_id',
        ),
        migrations.RemoveField(
            model_name='tb_dimension_nameid_view_info_test',
            name='nameid_view_id',
        ),
        migrations.DeleteModel(
            name='tb_dimension_nameid_view_device_info_test',
        ),
        migrations.DeleteModel(
            name='tb_dimension_nameid_view_info_test',
        ),
    ]
