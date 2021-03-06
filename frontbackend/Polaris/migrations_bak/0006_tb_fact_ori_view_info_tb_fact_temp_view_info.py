# Generated by Django 2.1.2 on 2019-05-08 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Polaris', '0005_auto_20190507_0727'),
    ]

    operations = [
        migrations.CreateModel(
            name='tb_fact_ori_view_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_address', models.CharField(max_length=256)),
                ('end_address', models.CharField(max_length=256)),
                ('country', models.CharField(max_length=256)),
                ('province', models.CharField(max_length=256)),
                ('city', models.CharField(max_length=256)),
                ('isp', models.CharField(max_length=256)),
                ('unknow_a', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='tb_fact_temp_view_info',
            fields=[
                ('view_id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('view_father_id', models.IntegerField(default=0)),
                ('view_default', models.CharField(max_length=256)),
                ('view_province', models.CharField(max_length=256)),
                ('view_city', models.CharField(max_length=256)),
                ('view_grade_name', models.CharField(max_length=256)),
                ('view_grade', models.IntegerField(default=0)),
                ('view_father_grade', models.IntegerField(default=0)),
                ('view_country', models.CharField(max_length=256)),
                ('view_region', models.CharField(max_length=256)),
                ('view_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Polaris.tb_fact_viewtype_info')),
            ],
        ),
    ]
