# Generated by Django 2.1.2 on 2019-05-15 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Polaris', '0038_auto_20190515_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tb_fact_dnstype_info',
            name='dns_status',
            field=models.CharField(choices=[('enable', 'enable'), ('disable', 'disable')], max_length=256),
        ),
    ]
