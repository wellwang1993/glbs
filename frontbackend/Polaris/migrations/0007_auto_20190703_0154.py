# Generated by Django 2.1.2 on 2019-07-03 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Polaris', '0006_tb_fact_user_info_uuid'),
    ]

    operations = [
        migrations.CreateModel(
            name='tb_fact_backend_dnszone_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internet_type', models.CharField(max_length=256)),
                ('record_type', models.CharField(max_length=256)),
                ('record_content', models.CharField(max_length=256)),
                ('record_name', models.CharField(max_length=256)),
                ('record_ttl', models.IntegerField(default=120)),
                ('dns_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Polaris.tb_fact_dnstype_info')),
            ],
        ),
        migrations.AlterField(
            model_name='tb_fact_zonetype_info',
            name='zone_status',
            field=models.CharField(choices=[('enable', 'enable'), ('disable', 'disable')], max_length=256),
        ),
        migrations.AddField(
            model_name='tb_fact_backend_dnszone_info',
            name='zone_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Polaris.tb_fact_zonetype_info'),
        ),
    ]
