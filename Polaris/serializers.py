# -*- coding: utf-8 -*-
from rest_framework import serializers
from Polaris.models import tb_fact_nameid_info,tb_fact_dnstype_info,tb_fact_dnszone_info,tb_fact_nameidpolicy_info,tb_fact_viewtype_info,tb_fact_view_info,tb_dimension_nameid_view_info,tb_dimension_nameid_view_device_info,tb_fact_device_info,tb_dimension_nameid_view_cname_info,tb_fact_cname_info,tb_fact_adminip_info,tb_fact_detecttask_info,tb_fact_detectdeviceavailability_info,tb_fact_detectdeviceavailability_standard_info
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


#如果使用该类的话，则在上传zone内容的时候需要手写zone的内容
class NameidDnsRelationinfo(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_dnstype_info
        fields = ['dns_name'] 
class NameidPolicyRelationinfo(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_nameidpolicy_info
        fields = ['policy_name']
class NameidListSerializer(serializers.ModelSerializer):
    #这种就是展示zone的所有内容
   # zone_type = DnszoneSerializer()
    #这个就是只展示关键字段zone_name.推荐这种
   # zone_type = NameidDnszoneRelationinfo()
    dns_type = NameidDnsRelationinfo()
    nameid_policy = NameidPolicyRelationinfo()
    class Meta:
        model = tb_fact_nameid_info
        fields = '__all__'
class NameidUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_nameid_info
        fields = '__all__'

class ViewtypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_viewtype_info
        fields = '__all__'
class ViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_view_info
        fields = '__all__'
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
class ViewtoNamiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_view_info
        fields = ['view_name']
class NameidViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_dimension_nameid_view_info
        fields = '__all__'
class NameidViewDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_dimension_nameid_view_device_info
        fields = '__all__' 
#为内部使用的序列化接口，支持筛选nameid对应的view和设备信息
class PartNameidSerializer(serializers.ModelSerializer):
     class Meta:
        model = tb_fact_nameid_info
        fields = ['nameid_name']
class PartVipDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_device_info
        fields = ['vip_address']
class PartViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_view_info
        fields = ['view_id','view_name']
class NameidViewDeviceListSerializer(serializers.ModelSerializer):
    nameid_view_id = PartViewSerializer()
    nameid_device_id = PartVipDeviceSerializer()
    nameid_id = PartNameidSerializer()
    class Meta:
        model = tb_dimension_nameid_view_device_info
        fields = ['nameid_id','nameid_view_id','nameid_device_id','nameid_device_ratio'] 
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
        fields = ['nameid_id','nameid_view_id','nameid_cname_id','nameid_cname_ratio']
class NameidCnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_cname_info
        fields = '__all__'
class NameidViewCnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_dimension_nameid_view_cname_info
        fields = '__all__'

#node和admin的对应关系
class AdminIpSerializer(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_adminip_info
        fields = '__all__'
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
