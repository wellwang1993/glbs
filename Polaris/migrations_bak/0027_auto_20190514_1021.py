# Generated by Django 2.1.2 on 2019-05-14 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Polaris', '0026_auto_20190514_1020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tb_fact_dnszone_info',
            name='dns_type',
        ),
        migrations.RemoveField(
            model_name='tb_fact_dnszone_info',
            name='internet_type',
        ),
        migrations.RemoveField(
            model_name='tb_fact_dnszone_info',
            name='record_content',
        ),
        migrations.RemoveField(
            model_name='tb_fact_dnszone_info',
            name='record_name',
        ),
        migrations.RemoveField(
            model_name='tb_fact_dnszone_info',
            name='record_ttl',
        ),
    ]