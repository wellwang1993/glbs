# Generated by Django 2.1.2 on 2019-06-19 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Polaris', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tb_fact_nameid_infos',
            name='dns_type',
        ),
        migrations.RemoveField(
            model_name='tb_fact_nameid_infos',
            name='nameid_policy',
        ),
        migrations.RemoveField(
            model_name='tb_fact_nameid_infos',
            name='zone_type',
        ),
        migrations.DeleteModel(
            name='tb_fact_nameid_infos',
        ),
    ]
