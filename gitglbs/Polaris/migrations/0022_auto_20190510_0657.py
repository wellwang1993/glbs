# Generated by Django 2.1.2 on 2019-05-10 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Polaris', '0021_auto_20190510_0654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tb_dimension_nameid_view_info',
            name='nameid_view_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Polaris.tb_fact_temp_view_info'),
        ),
    ]
