# -*- coding: utf-8 -*-
from rest_framework import serializers
from glbs.models import tb_fact_nameid_info,tb_fact_dnstype_info,tb_fact_dnszone_info,tb_fact_nameidpolicy_info,tb_fact_viewtype_info,tb_fact_view_info,tb_dimension_nameid_view_info,tb_dimension_nameid_view_device_info,tb_fact_device_info
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
class NameidDnszoneRelationinfo(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_dnszone_info
        fields = ['zone_name'] 
class NameidPolicyRelationinfo(serializers.ModelSerializer):
    class Meta:
        model = tb_fact_nameidpolicy_info
        fields = ['policy_name']
class NameidListSerializer(serializers.ModelSerializer):
    #这种就是展示zone的所有内容
   # zone_type = DnszoneSerializer()
    #这个就是只展示关键字段zone_name.推荐这种
    zone_type = NameidDnszoneRelationinfo()
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
