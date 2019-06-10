# -*- coding: utf-8 -*-
from rest_framework import serializers
from Polaris.models import tb_fact_dnszone_info,tb_fact_nameid_info,tb_fact_dnstype_info,tb_fact_nameidpolicy_info,tb_fact_viewtype_info,tb_dimension_nameid_view_info,tb_dimension_nameid_view_device_info,tb_fact_device_info,tb_dimension_nameid_view_cname_info,tb_fact_cname_info,tb_fact_adminip_info,tb_fact_detecttask_info,tb_fact_detectdeviceavailability_info,tb_fact_detectdeviceavailability_standard_info,tb_fact_temp_view_info,tb_fact_dnsip_info
class DnstypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_dnstype_info
        fields = '__all__'
class DnszoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_dnszone_info
        fields = '__all__'
class NameidPolciySerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_nameidpolicy_info
        fields = '__all__'

#对nameid的序列化
#如果使用该类的话，则在上传zone内容的时候需要手写zone的内容
class NameidDnsRelationinfo(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_dnstype_info
        fields = ['dns_name'] 
class NameidPolicyRelationinfo(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_nameidpolicy_info
        fields = ['policy_name']
class NameidZoneRelationinfo(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_dnszone_info
        fields = ['zone_name']
class NameidListSerializer(serializers.ModelSerializer):
    #只展示关键的字段既可以
    zone_type = NameidZoneRelationinfo()
    dns_type = NameidDnsRelationinfo()
    nameid_policy = NameidPolicyRelationinfo()
    class Meta:
        model = tb_fact_nameid_info
        fields = '__all__'
import re
class NameidUpdateSerializer(serializers.ModelSerializer):
    nameid_name =  serializers.CharField()
    def validate_nameid_name(self,nameid_name):
         pat_domain = re.compile(r"([a-zA-Z0-9][-a-zA-Z0-9]{0,62}(.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+.?)")
         if not pat_domain.match(nameid_name):
             raise serializers.ValidationError("域名格式错误")
         return nameid_name
         #pat_domain = re.compile(r"([a-zA-Z0-9][-a-zA-Z0-9]{0,62}(.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+.?)")
         #if not pat_domain.match(nameid_name):
         #   raise serializers.ValidationError("域名格式错误")
         #return nameid_name
    class Meta:
        model = tb_fact_nameid_info
        fields = '__all__'
#对dns的ip的管理
class DnsIpListSerializer(serializers.ModelSerializer):
    dns_type = NameidDnsRelationinfo()
    class Meta:
        model = tb_fact_dnsip_info
        fields = '__all__'
class DnsIpUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_dnsip_info
        fields = '__all__'
#对dnszone的管理
class DnszoneListSerializer(serializers.ModelSerializer):
    dns_type = NameidDnsRelationinfo()
    class Meta:
        model = tb_fact_dnszone_info
        fields = '__all__'
class DnszoneUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_dnszone_info
        fields = '__all__'
#view相关的序列化
class ViewtypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_viewtype_info
        fields = '__all__'
class ViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_temp_view_info
        fields = '__all__'
#虚拟设备的序列化
class VipDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_device_info
        fields = '__all__'
'''
class VipDeviceTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_temp_device_info
        fields = '__all__'
'''
#nameid,view的序列化
class NameidViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_dimension_nameid_view_info
        fields = '__all__'

#nameid,view,device的序列化
class NameidViewDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_dimension_nameid_view_device_info
        fields = '__all__' 
#为内部使用的序列化接口，支持筛选nameid对应的view和设备信息
class PartNameidSerializer(serializers.ModelSerializer):
     class Meta:
        model = tb_fact_nameid_info
        fields = ['id','nameid_name']
class PartVipDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_device_info
        fields = ['id','vip_address']
class PartViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_temp_view_info
        fields = ['id','view_default','view_country','view_isp','view_region','view_province','view_city']

class NameidViewListSerializer(serializers.ModelSerializer):
    nameid_view_id = PartViewSerializer()
    nameid_id = PartNameidSerializer()
    class Meta:
        model = tb_dimension_nameid_view_info
        fields = '__all__'

class NameidViewDeviceListSerializer(serializers.ModelSerializer):
    nameid_view_id = PartViewSerializer()
    nameid_device_id = PartVipDeviceSerializer()
    nameid_id = PartNameidSerializer()
    class Meta:
        model = tb_dimension_nameid_view_device_info
        fields = ['id','nameid_id','nameid_view_id','nameid_device_id','nameid_device_ratio'] 
#为内部使用的序列化接口，支持筛选nameid对应的view和cname信息
class PartNameidCnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_cname_info
        fields = ['nameid_cname']
class NameidViewCnameListSerializer(serializers.ModelSerializer):
    nameid_id = PartNameidSerializer()
    nameid_view_id = PartViewSerializer()
    nameid_cname_id = PartNameidCnameSerializer()
    class Meta:
        model = tb_dimension_nameid_view_cname_info
        fields = ['id','nameid_id','nameid_view_id','nameid_cname_id','nameid_cname_ratio']

#cname的序列化
class NameidCnameSerializer(serializers.ModelSerializer):
    nameid_cname =  serializers.CharField()
    def validate_nameid_cname(self,nameid_cname):
         pat_domain = re.compile(r"([a-zA-Z0-9][-a-zA-Z0-9]{0,62}(.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+.?)")
         if not pat_domain.match(nameid_cname):
            raise serializers.ValidationError("域名格式错误")
         return nameid_cname
    class Meta:
        model = tb_fact_cname_info
        fields = '__all__'
#nameid,view.cname的序列化
class NameidViewCnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_dimension_nameid_view_cname_info
        fields = '__all__'

#node和admin的对应关系
class AdminIpSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_adminip_info
        fields = '__all__'
#探测任务描述的序列化
class DetectTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_detecttask_info
        fields = '__all__'
class DetectDeviceAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_detectdeviceavailability_info
        fields = '__all__'
class DetectDeviceAvailabilityStandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_detectdeviceavailability_standard_info
        fields = '__all__'


