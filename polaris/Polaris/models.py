# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models

#存储dns类型的，id是自增主键,相当于是dns的类型
class tb_fact_dnstype_info(models.Model):
        status_choice = (
        ('enable','enable'),
        ('disable','disable'),
        )
        dns_name = models.CharField(max_length = 254,unique=True)
        dns_status = models.CharField(max_length = 256,choices=status_choice)
        dns_describe = models.CharField(max_length = 256)
        def __str__(self):
            return self.dns_name
#存储dnsip的
class tb_fact_dnsip_info(models.Model):
        status_choice = (
        ('enable','enable'),
        ('disable','disable'),
        )
        dns_ip = models.CharField(max_length = 150,unique=True)
        dns_status = models.CharField(max_length = 256,choices=status_choice)
        dns_describe = models.CharField(max_length = 256)
        dns_type = models.ForeignKey('tb_fact_dnstype_info',on_delete=models.CASCADE)
        def __str__(self):
            return self.dns_ip

class tb_fact_zonetype_info(models.Model):
        status_choice = (
       # ('enable','enable'),
        ('disable','disable'),
        )
        zone_name = models.CharField(max_length = 150,unique=True)
        zone_status = models.CharField(max_length = 256,choices=status_choice)
        zone_describe = models.CharField(max_length = 256)
        def __str__(self):
            return self.zone_name

#存储zone类型的，dns_type作为外键 
class tb_fact_dnszone_info(models.Model):
        internet_type = models.CharField(max_length = 256) 
        record_type = models.CharField(max_length = 256)
        dns_type = models.ForeignKey('tb_fact_dnstype_info',on_delete=models.CASCADE)
        record_content = models.CharField(max_length = 256)
        zone_name = models.ForeignKey('tb_fact_zonetype_info',on_delete=models.CASCADE)    
      #  zone_name = models.CharField(max_length = 256)
        record_name = models.CharField(max_length = 256)
        record_ttl = models.IntegerField(default=120)
        def __str__(self):
            return self.zone_name
#存储nameid策略的,后续nameid在选择策略的时候必须从这里选择，支持default,fuse等策略
class tb_fact_nameidpolicy_info(models.Model):
        status_choice = (
        ('enable','enable'),
        ('disable','disable'),
        )
        policy_name = models.CharField(max_length = 254,unique=True)
        policy_status = models.CharField(max_length = 256,choices=status_choice)
        policy_describe = models.CharField(max_length = 256)
        def __str__(self):
            return self.policy_name
#存储nameid的，dns_type作为外键,默认id作为主键
class tb_fact_nameid_info(models.Model):
        status_choice = (
      #  ('enable','enable'),
        ('disable','disable'),
        )
        nameid_name = models.CharField(max_length = 254,unique=True)
        zone_type = models.ForeignKey('tb_fact_zonetype_info',on_delete=models.CASCADE)
        dns_type = models.ForeignKey('tb_fact_dnstype_info',on_delete=models.CASCADE)
        nameid_status = models.CharField(max_length = 256,choices=status_choice) 
        nameid_policy = models.ForeignKey('tb_fact_nameidpolicy_info',on_delete=models.CASCADE)
        def __str__(self):
            return self.nameid_name
'''
class tb_fact_nameid_infos(models.Model):
        status_choice = (
        ('enable','enable'),
        ('disable','disable'),
        )
        nameid_name = models.CharField(max_length = 254,unique=True)
        zone_type = models.ForeignKey('tb_fact_zonetype_info',on_delete=models.CASCADE)
        #zone_type = models.ForeignKey('tb_fact_dnszone_info',on_delete=models.CASCADE,default='')
        dns_type = models.ForeignKey('tb_fact_dnstype_info',on_delete=models.CASCADE)
        nameid_status = models.CharField(max_length = 256,choices=status_choice) 
        nameid_policy = models.ForeignKey('tb_fact_nameidpolicy_info',on_delete=models.CASCADE)
        def __str__(self):
            return self.nameid_name
'''
#对view的管理
#view级别的,增加这张表用于支持不同的地址库，比如将来有新的地址库接入进来，那他们view应该是完全不同的
class tb_fact_viewtype_info(models.Model):
	view_type = models.CharField(max_length = 256)	
	view_describe = models.CharField(max_length = 256)
	def __str__(self):
        	return self.view_type
#对view的管理
class tb_fact_temp_view_info(models.Model):
    view_father_id = models.IntegerField(default = 0)
    view_default = models.CharField(max_length = 256,default='*')
    view_country = models.CharField(max_length = 256,default='*')
    view_isp = models.CharField(max_length = 256,default='*')
    view_region = models.CharField(max_length = 256,default='*')
    view_province = models.CharField(max_length = 256,default='*')
    view_city = models.CharField(max_length = 256,default='*')
    view_grade_name = models.CharField(max_length = 256,default='*')
    view_grade = models.IntegerField(default = 0)
    view_father_grade = models.IntegerField(default = 0)
    view_type = models.ForeignKey('tb_fact_viewtype_info',on_delete=models.CASCADE)
    def __str__(self):
        return "{}-{}-{}-{}-{}-{}".format(self.view_country,self.view_isp,self.view_region,self.view_province,self.view_city,self.view_grade_name)
'''
class tb_fact_view_info(models.Model):
	view_id = models.IntegerField(default = 0,primary_key=True)
	view_father_id = models.IntegerField(default = 0)
	view_name = models.CharField(max_length = 256)
	view_en_name = models.CharField(max_length = 256)
	view_grade_name = models.CharField(max_length = 256)
	view_grade = models.IntegerField(default = 0)
	view_father_grade = models.IntegerField(default = 0)
	view_type = models.ForeignKey('tb_fact_viewtype_info',on_delete=models.CASCADE)
	def __str__(self):
		return self.view_name
'''
#对设备的管理
class tb_fact_device_info(models.Model):
        vip_status_choice = (
        ('enable','enable'),
        ('disable','disable'),
        )
        switch_status_choice = (
        ('enable','enable'),
        ('disable','disable'),
        )
        node_id = models.CharField(max_length = 256,default='0')
        vip_status = models.CharField(max_length = 256,choices =vip_status_choice)
        vip_address = models.CharField(max_length = 150,unique=True)
        vip_bandwidth = models.CharField(max_length = 256)
        vip_enable_switch = models.CharField(max_length = 256,default='enable',choices =switch_status_choice)
        node_country = models.CharField(max_length = 256,default="0")
        node_isp = models.CharField(max_length = 256,default="0")
        node_region = models.CharField(max_length = 256,default="0")
        node_province = models.CharField(max_length = 256,default="0")
        node_city = models.CharField(max_length = 256,default='0')
        def __str__(self):
            return self.vip_address        
class tb_fact_realdevice_info(models.Model):
	ip_status = models.CharField(max_length = 256)
	ip_address = models.CharField(max_length = 256)
	ip_bandwidth = models.CharField(max_length = 256)	
	def __str__(self):
		return self.ip_address
class tb_dimension_device_info(models.Model):
	vip_id = models.ForeignKey('tb_fact_device_info',on_delete=models.CASCADE)
	vip_address = models.CharField(max_length = 256)
	realip_address = models.CharField(max_length = 256)
	def __str__(self):
		return self.vip_address
#对服务的管理
#域名和 view的关系

class tb_dimension_nameid_view_info(models.Model):
        resolve_type_choice = (
        ('cname','cname'),
        ('a','a'),
        ('aaaa','aaaa'),
        )
        preferred_type_choice = (
        ('rr','rr'),
        ('ratio','ratio'),
        )
        status_choice = (
        ('enable','enable'),
        ('disable','disable'),
        )
        nameid_id = models.ForeignKey('tb_fact_nameid_info',on_delete=models.CASCADE)
        nameid_view_id = models.ForeignKey('tb_fact_temp_view_info',on_delete=models.CASCADE)
        nameid_resolve_type = models.CharField(max_length=10,choices=resolve_type_choice,default='a')
        nameid_max_ip = models.IntegerField(default = 1)
        nameid_preferred = models.CharField(max_length=10,choices=preferred_type_choice,default="rr")
        nameid_status = models.CharField(max_length = 256,choices=status_choice,default="enable")
        nameid_ttl = models.IntegerField(default = 120)
        class Meta:
            unique_together = ('nameid_id','nameid_view_id')
        def __str__(self):
            return "{}-{}-{}".format(self.nameid_id,self.nameid_view_id,self.nameid_preferred)
import json
#域名和view和设备的关系
class tb_dimension_nameid_view_device_info(models.Model):
        status_choice = (
        ('enable','enable'),
        ('disable','disable'),
        )
        nameid_id = models.ForeignKey('tb_fact_nameid_info',on_delete=models.CASCADE)
        nameid_view_id = models.ForeignKey('tb_fact_temp_view_info',on_delete=models.CASCADE)	
        nameid_device_id = models.ForeignKey('tb_fact_device_info',on_delete=models.CASCADE)
        nameid_device_ratio = models.IntegerField(default = 1)
        nameid_device_status = models.CharField(max_length = 256,choices=status_choice)
        class Meta:
            ordering = ['id']
            unique_together = ('nameid_id','nameid_view_id','nameid_device_id')
       # def __str__(self):
       #     return json.dumps({"nameid_id":self.nameid_id,"nameid_view_id":self.nameid_view_id,"nameid_device_id":self.nameid_device_id,"nameid_device_ratio":self.nameid_device_ratio,"nameid_device_status":self.nameid_device_status})
           # return "{}_{}_{}".format(self.nameid_id,self.nameid_view_id,self.nameid_device_id)
#cname信息
class tb_fact_cname_info(models.Model):
        nameid_cname = models.CharField(max_length = 250,unique=True)
        nameid_owner = models.CharField(max_length = 256)
        nameid_supplier = models.CharField(max_length = 256)
        nameid_business = models.CharField(max_length = 256)
        def __str__(self):
            return self.nameid_cname
#域名和view和cname的关系
class tb_dimension_nameid_view_cname_info(models.Model):
        status_choice = (
        ('enable','enable'),
        ('disable','disable'),
        )
        nameid_id = models.ForeignKey('tb_fact_nameid_info',on_delete=models.CASCADE)
        nameid_view_id = models.ForeignKey('tb_fact_temp_view_info',on_delete=models.CASCADE)	
        nameid_cname_id = models.ForeignKey('tb_fact_cname_info',on_delete=models.CASCADE)
        nameid_cname_ratio = models.IntegerField(default = 1)
        nameid_cname_status = models.CharField(max_length = 256,choices=status_choice)
        class Meta:
            unique_together = ('nameid_id','nameid_view_id','nameid_cname_id')
        def __str__(self):
            return "{}-{}-{}".format(self.nameid_id,self.nameid_view_id,self.nameid_cname_id)

#node和adminip的对应关系。用于设备探测
class tb_fact_adminip_info(models.Model):
        status_choice = (
        ('enable','enable'),
        ('disable','disable'),
        )
        node_id = models.CharField(max_length = 256,default='0')
        admin_ip = models.CharField(max_length = 150,unique=True)
        country = models.CharField(max_length = 256,default='0')
        isp = models.CharField(max_length = 256)
        region = models.CharField(max_length = 256)
        province = models.CharField(max_length = 256)
        city = models.CharField(max_length = 256,default='0')
        availability_status = models.CharField(max_length = 256,choices=status_choice,default = "disable")
        qos_status = models.CharField(max_length = 256,choices=status_choice,default = "disable")
        def __str__(self):
                return self.admin_ip
#描述探测任务的
class tb_fact_detecttask_info(models.Model):
        unit_choice = (
        ('second','second'),
        ('minute','minute'),
        ('hour','hour'),
        ('day','day'),
        ('week','week'),
        ('month','month'),
        )
        detect_name = models.CharField(max_length = 150,unique=True)
        detect_frency = models.IntegerField()
        detect_frency_unit = models.CharField(max_length = 256,choices=unit_choice,default='second')
        effective_time = models.IntegerField(default=15)
        effective_time_unit = models.CharField(max_length = 256,choices=unit_choice,default='second')
#上传探测的设备可用性数据的
class tb_fact_detectdeviceavailability_info(models.Model):
        status_choice = (
        ('enable','enable'),
        ('disable','disable'),
        )
        admin_ip = models.CharField(max_length = 256)
        vip_address  = models.CharField(max_length = 256)
        availability = models.CharField(max_length = 256,choices=status_choice)
        admin_isp = models.CharField(max_length = 256,default='0')
        create_time = models.DateTimeField(auto_now = True)
class tb_fact_detectdeviceavailability_select_info(models.Model):
        status_choice = (
        ('enable','enable'),
        ('disable','disable'),
        )
        admin_ip = models.CharField(max_length = 256)
        vip_address  = models.CharField(max_length = 256)
        availability = models.CharField(max_length = 256,choices=status_choice)
        admin_isp = models.CharField(max_length = 256,default='0')
        create_time = models.DateTimeField(auto_now = True)
#针对设备可用性的探测数据，该表是这些数据是否有效的描述，是一个标准
class tb_fact_detectdeviceavailability_standard_info(models.Model):
        node_isp = models.CharField(max_length = 150,unique=True)
        total_value = models.IntegerField()
        absolute_value = models.IntegerField()
        relative_rate = models.FloatField(default=0.0)
#对geoip库原始数据的录入
class tb_fact_ori_view_info(models.Model):
        start_address = models.CharField(max_length = 256)
        end_address = models.CharField(max_length = 256)
        country = models.CharField(max_length = 256)
        region = models.CharField(max_length = 256,default='0')
        province = models.CharField(max_length = 256)
        city = models.CharField(max_length = 256)
        unknow_a = models.CharField(max_length = 30,default="0")
        isp = models.CharField(max_length = 256)
        unknow_b = models.CharField(max_length = 30,default="0")
        unknow_c = models.CharField(max_length = 30,default="0")
        unknow_d = models.CharField(max_length = 30,default="0")
        unknow_e = models.CharField(max_length = 30,default="0")
        unknow_f = models.CharField(max_length = 30,default="0")
        unknow_g = models.CharField(max_length = 30,default="0")
        unknow_h = models.CharField(max_length = 30,default="0")
        unknow_i = models.CharField(max_length = 30,default="0")
        unknow_j = models.CharField(max_length = 30,default="0")
        unknow_k = models.CharField(max_length = 30,default="0")
        unknow_l = models.CharField(max_length = 30,default="0")
        unknow_m = models.CharField(max_length = 30,default="0")
#对地址库的管理
class tb_fact_ipset_info(models.Model):
        view_id = models.ForeignKey('tb_fact_temp_view_info',on_delete=models.CASCADE) 
        start_address = models.CharField(max_length = 256)
        end_address = models.CharField(max_length = 256)
