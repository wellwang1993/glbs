# Generated by Django 2.1.2 on 2019-05-14 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Polaris', '0028_delete_tb_fact_dnszone_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='tb_fact_dnszone_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internet_type', models.CharField(max_length=256)),
                ('record_content', models.CharField(max_length=256)),
                ('zone_name', models.CharField(max_length=256)),
                ('record_name', models.CharField(max_length=256)),
                ('record_ttl', models.IntegerField(default=120)),
                ('dns_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Polaris.tb_fact_dnstype_info')),
            ],
        ),
    ]
