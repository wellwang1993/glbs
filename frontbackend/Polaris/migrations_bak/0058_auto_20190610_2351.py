# Generated by Django 2.1.2 on 2019-06-10 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Polaris', '0057_auto_20190602_0233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tb_fact_detecttask_info',
            name='detect_name',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]