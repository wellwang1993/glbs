# Generated by Django 2.1.2 on 2019-05-22 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Polaris', '0045_auto_20190522_0606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tb_fact_adminip_info',
            name='admin_ip',
            field=models.CharField(max_length=254, unique=True),
        ),
    ]
