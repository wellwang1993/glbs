# Generated by Django 2.1.2 on 2019-05-09 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Polaris', '0013_tb_fact_temp_view_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tb_fact_temp_view_info',
            name='view_city',
            field=models.CharField(default='*', max_length=256),
        ),
        migrations.AlterField(
            model_name='tb_fact_temp_view_info',
            name='view_country',
            field=models.CharField(default='*', max_length=256),
        ),
        migrations.AlterField(
            model_name='tb_fact_temp_view_info',
            name='view_default',
            field=models.CharField(default='*', max_length=256),
        ),
        migrations.AlterField(
            model_name='tb_fact_temp_view_info',
            name='view_grade_name',
            field=models.CharField(default='*', max_length=256),
        ),
        migrations.AlterField(
            model_name='tb_fact_temp_view_info',
            name='view_isp',
            field=models.CharField(default='*', max_length=256),
        ),
        migrations.AlterField(
            model_name='tb_fact_temp_view_info',
            name='view_province',
            field=models.CharField(default='*', max_length=256),
        ),
        migrations.AlterField(
            model_name='tb_fact_temp_view_info',
            name='view_region',
            field=models.CharField(default='*', max_length=256),
        ),
    ]