# Generated by Django 2.1.2 on 2019-04-23 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glbs', '0002_auto_20190423_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tb_fact_nameidpolicy_info',
            name='policy_name',
            field=models.CharField(max_length=254, unique=True),
        ),
    ]
