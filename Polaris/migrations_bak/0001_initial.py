# Generated by Django 2.1.2 on 2019-05-06 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tb_dimension_device_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vip_address', models.CharField(max_length=256)),
                ('realip_address', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='tb_dimension_nameid_view_cname_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameid_cname_ratio', models.IntegerField(default=1)),
                ('nameid_cname_status', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='tb_dimension_nameid_view_device_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameid_device_ratio', models.IntegerField(default=1)),
                ('nameid_device_status', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='tb_dimension_nameid_view_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameid_resolve_type', models.CharField(choices=[('cname', 'cname'), ('a', 'a'), ('aaaa', 'aaaa')], default='a', max_length=10)),
                ('nameid_max_ip', models.IntegerField(default=1)),
                ('nameid_preferred', models.CharField(choices=[('rr', 'rr'), ('ratio', 'ratio')], default='rr', max_length=10)),
                ('nameid_status', models.CharField(max_length=256)),
                ('nameid_ttl', models.IntegerField(default=120)),
            ],
        ),
        migrations.CreateModel(
            name='tb_fact_adminip_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node_id', models.IntegerField()),
                ('admin_ip', models.CharField(max_length=256)),
                ('isp', models.CharField(max_length=256)),
                ('region', models.CharField(max_length=256)),
                ('province', models.CharField(max_length=256)),
                ('status', models.CharField(default='disable', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='tb_fact_cname_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameid_cname', models.CharField(max_length=256)),
                ('nameid_owner', models.CharField(max_length=256)),
                ('nameid_supplier', models.CharField(max_length=256)),
                ('nameid_business', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='tb_fact_detectdeviceavailability_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_ip', models.CharField(max_length=256)),
                ('vip_address', models.CharField(max_length=256)),
                ('availability', models.CharField(max_length=256)),
                ('admin_isp', models.CharField(default='0', max_length=256)),
                ('create_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='tb_fact_detectdeviceavailability_standard_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node_isp', models.CharField(max_length=256)),
                ('total_value', models.IntegerField()),
                ('absolute_value', models.IntegerField()),
                ('relative_rate', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='tb_fact_detecttask_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detect_name', models.CharField(max_length=256)),
                ('detect_frency', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='tb_fact_device_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node_id', models.IntegerField(default=0)),
                ('vip_status', models.CharField(max_length=256)),
                ('vip_address', models.CharField(max_length=256)),
                ('vip_bandwidth', models.CharField(max_length=256)),
                ('vip_enable_switch', models.CharField(default='enable', max_length=256)),
                ('node_isp', models.CharField(default='0', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='tb_fact_dnstype_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dns_name', models.CharField(max_length=254, unique=True)),
                ('dns_status', models.CharField(max_length=256)),
                ('dns_describe', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='tb_fact_dnszone_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zone_name', models.CharField(max_length=256)),
                ('zone_soa', models.CharField(max_length=256)),
                ('ns_name', models.CharField(max_length=256)),
                ('ns_address', models.CharField(max_length=256)),
                ('ns_ttl', models.IntegerField(default=120)),
                ('dns_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Polaris.tb_fact_dnstype_info')),
            ],
        ),
        migrations.CreateModel(
            name='tb_fact_nameid_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameid_name', models.CharField(max_length=254, unique=True)),
                ('nameid_status', models.CharField(max_length=256)),
                ('dns_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Polaris.tb_fact_dnstype_info')),
            ],
        ),
        migrations.CreateModel(
            name='tb_fact_nameidpolicy_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy_name', models.CharField(max_length=254, unique=True)),
                ('policy_status', models.CharField(max_length=256)),
                ('policy_describe', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='tb_fact_realdevice_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_status', models.CharField(max_length=256)),
                ('ip_address', models.CharField(max_length=256)),
                ('ip_bandwidth', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='tb_fact_view_info',
            fields=[
                ('view_id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('view_father_id', models.IntegerField(default=0)),
                ('view_name', models.CharField(max_length=256)),
                ('view_en_name', models.CharField(max_length=256)),
                ('view_grade_name', models.CharField(max_length=256)),
                ('view_grade', models.IntegerField(default=0)),
                ('view_father_grade', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='tb_fact_viewtype_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view_type', models.CharField(max_length=256)),
                ('view_describe', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='tb_temp_device_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vip_address', models.CharField(max_length=250, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='tb_fact_view_info',
            name='view_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Polaris.tb_fact_viewtype_info'),
        ),
        migrations.AddField(
            model_name='tb_fact_nameid_info',
            name='nameid_policy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Polaris.tb_fact_nameidpolicy_info'),
        ),
        migrations.AddField(
            model_name='tb_dimension_nameid_view_info',
            name='nameid_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Polaris.tb_fact_nameid_info'),
        ),
        migrations.AddField(
            model_name='tb_dimension_nameid_view_info',
            name='nameid_view_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Polaris.tb_fact_view_info'),
        ),
        migrations.AddField(
            model_name='tb_dimension_nameid_view_device_info',
            name='nameid_device_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Polaris.tb_temp_device_info'),
        ),
        migrations.AddField(
            model_name='tb_dimension_nameid_view_device_info',
            name='nameid_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Polaris.tb_fact_nameid_info'),
        ),
        migrations.AddField(
            model_name='tb_dimension_nameid_view_device_info',
            name='nameid_view_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Polaris.tb_fact_view_info'),
        ),
        migrations.AddField(
            model_name='tb_dimension_nameid_view_cname_info',
            name='nameid_cname_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Polaris.tb_fact_cname_info'),
        ),
        migrations.AddField(
            model_name='tb_dimension_nameid_view_cname_info',
            name='nameid_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Polaris.tb_fact_nameid_info'),
        ),
        migrations.AddField(
            model_name='tb_dimension_nameid_view_cname_info',
            name='nameid_view_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Polaris.tb_fact_view_info'),
        ),
        migrations.AddField(
            model_name='tb_dimension_device_info',
            name='vip_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Polaris.tb_fact_device_info'),
        ),
        migrations.AlterUniqueTogether(
            name='tb_dimension_nameid_view_info',
            unique_together={('nameid_id', 'nameid_view_id')},
        ),
        migrations.AlterUniqueTogether(
            name='tb_dimension_nameid_view_device_info',
            unique_together={('nameid_id', 'nameid_view_id', 'nameid_device_id')},
        ),
        migrations.AlterUniqueTogether(
            name='tb_dimension_nameid_view_cname_info',
            unique_together={('nameid_id', 'nameid_view_id', 'nameid_cname_id')},
        ),
    ]
