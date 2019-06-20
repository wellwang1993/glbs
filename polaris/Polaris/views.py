# -*- coding: utf-8 -*-
from Polaris.utils.glbscache import read_from_cache_cluster,get_keys_from_cache
from rest_framework.decorators import action
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Count
from Polaris.utils.rawsql import my_custom_sql
from Polaris.utils.download import urllib_post,urllib_get
from django.db import IntegrityError, transaction
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet
from Polaris.serializers import DnstypeSerializer,DnszoneListSerializer,DnszoneUpdateSerializer,NameidPolciySerializer,NameidListSerializer,NameidUpdateSerializer,ViewtypeSerializer,ViewSerializer,NameidViewSerializer,NameidViewDeviceSerializer,VipDeviceSerializer,NameidViewDeviceSerializer,NameidViewDeviceListSerializer,NameidViewCnameSerializer,NameidCnameSerializer,NameidViewCnameListSerializer,AdminIpSerializer,DetectTaskSerializer,DetectDeviceAvailabilitySerializer,DetectDeviceAvailabilityStandardSerializer,DnsIpListSerializer,DnsIpUpdateSerializer,NameidViewListSerializer,DetectDeviceAvailabilitySelectSerializer,ZonetypeSerializer
from Polaris.models import tb_fact_nameid_info,tb_fact_dnszone_info,tb_fact_dnstype_info,tb_fact_nameidpolicy_info,tb_fact_viewtype_info,tb_dimension_nameid_view_info,tb_dimension_nameid_view_device_info,tb_fact_device_info,tb_dimension_nameid_view_device_info,tb_dimension_nameid_view_cname_info,tb_fact_cname_info,tb_fact_adminip_info,tb_fact_detecttask_info,tb_fact_detectdeviceavailability_info,tb_fact_detectdeviceavailability_standard_info,tb_fact_temp_view_info,tb_fact_dnsip_info,tb_fact_detectdeviceavailability_select_info,tb_fact_zonetype_info
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.views import APIView
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import Http404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.renderers import JSONRenderer
from django.db.models import Q
from django.http import HttpResponse
#from Polaris.utils.exception import Error
from django.db.transaction import set_rollback

class MyModelViewSet(viewsets.ModelViewSet):
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            is_valid = serializer.is_valid(raise_exception=False)
            if not is_valid:
                return Response({'code':0, 'msg':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            return Response({'code':1,'msg': serializer.data},status=status.HTTP_200_OK)        
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)        
    #调用自定义的异常，把API的异常集中到view层处理，而且需要把is_valid的raise_exception改成false,不然异常就卡在那里不往下走了
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            is_valid = serializer.is_valid(raise_exception=False)
            if not is_valid:
                return Response({'code':0, 'msg':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'code':1,'msg':[serializer.data]},status=status.HTTP_200_OK)        
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)        
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({'code':1,'msg': serializer.data},status=status.HTTP_200_OK)        
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)        
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response({'code':1,'msg': serializer.data},status=status.HTTP_200_OK)        
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)        
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'code':1,'msg':"delok"},status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)        

#支持增删查改zonetyep
class Zonetypeinfo(MyModelViewSet):
    queryset = tb_fact_zonetype_info.objects.all() 
    serializer_class = ZonetypeSerializer
    @action(detail=False,methods=['get'])

    @action(detail=False,methods=['get'])
    def push_zone(self,request):
        try:
            zone_id = request.GET.get('zone_id')
            if zone_id == None or len(zone_id) == 0:
                return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST)
            tb_fact_zonetype_info.objects.filter(id=zone_id).update(zone_status="enable")
            return Response({'code':1,'msg':"ok"},status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)
    @action(detail=False,methods=['get'])
    def universal_matching_zonetype(self,request):
        try:
            zonetype = request.GET.get('zonetype')
            queryset = tb_fact_zonetype_info.objects.all()
            if zonetype != None:
                queryset = queryset.filter(zone_name__contains = zonetype)
            serializer = self.serializer_class(queryset,many=True)
            return Response({'code':1,'msg': serializer.data},status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)
#支持增删查改dnstype
class Dnstypeinfo(MyModelViewSet):
    queryset = tb_fact_dnstype_info.objects.all()
    serializer_class = DnstypeSerializer
    #通过dnsname查找item
    @action(detail=False,methods=['get'])
    def universal_matching_dnstype(self,request):
        try:
            dnstype = request.GET.get('dnstype')
            queryset = tb_fact_dnstype_info.objects.all()
            if dnstype != None:
                queryset = queryset.filter(dns_name__contains = dnstype)
            serializer = self.serializer_class(queryset,many=True)
            return Response({'code':1,'msg': serializer.data},status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)
#支持增删查改dnsip
class DnsIpinfo(MyModelViewSet):
    queryset = tb_fact_dnsip_info.objects.all()
    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return DnsIpListSerializer
        return DnsIpUpdateSerializer
    #通过dnsip查找item
    @action(detail=False,methods=['get'])
    def universal_matching_dnsip(self,request):
        try:
            dnsip = request.GET.get('dnsip')
            queryset = tb_fact_dnsip_info.objects.all()
            if dnsip != None:
                queryset = queryset.filter(dns_ip__contains = dnsip)
            serializer = DnsIpListSerializer(queryset,many=True)
            return Response({'code':1,'msg': serializer.data},status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)

#支持增删查改zone
class Dnszoneinfo(MyModelViewSet):
    queryset = tb_fact_dnszone_info.objects.all()
    def get_serializer_class(self):
        if self.action in ['list','retrieve','universal_matching_dnszone']:
            return DnszoneListSerializer
        return DnszoneUpdateSerializer
    #支持通过zonename查找 item
    @action(detail=False,methods=['get'])
    def universal_matching_dnszone(self,request):
        try:
            zonename = request.GET.get('zonename')
            queryset = tb_fact_dnszone_info.objects.all()
            if zonename != None:
                queryset = queryset.filter(zone_name__contains = zonename)
            serializer = self.get_serializer(queryset,many=True)
            return Response({'code':1,'msg': serializer.data},status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)
#支持增删查改nameid的策略
class NameidPolciyinfo(MyModelViewSet):
    queryset = tb_fact_nameidpolicy_info.objects.all()
    serializer_class = NameidPolciySerializer
    #支持通过策略查找item
    @action(detail=False,methods=['get'])
    def universal_matching_nameidpolicy(self,request):
        try:
            policyname = request.GET.get('policyname')
            queryset = tb_fact_nameidpolicy_info.objects.all()
            if policyname != None:
                queryset = queryset.filter(policy_name__contains = policyname)
            serializer = self.get_serializer(queryset,many=True)
            return Response({'code':1,'msg': serializer.data},status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)

#支持增删查改设备vip
class VipDeviceinfo(MyModelViewSet):
    queryset = tb_fact_device_info.objects.all()
    serializer_class = VipDeviceSerializer
    
    @action(detail=False,methods=['get'])
    def get_all_resource_info(self,request):
         try:
            nodeid = request.GET.get('nodeid')
            ip = request.GET.get('ip')
            queryset = tb_fact_device_info.objects.all()
            if nodeid != None:
                queryset = queryset.filter(node_id__contains=nodeid)
            if ip != None:
                queryset = queryset.filter(vip_address__contains=ip)
            serializer = self.get_serializer(queryset,many=True)
            return Response({'code':1,'msg':serializer.data},status=status.HTTP_200_OK)
         except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST) 

    #维护资源上下线的时候
    @action(detail=False,methods=['post'])
    def maintain_resource(self,request):
        record_list = []
        try:
            with transaction.atomic():            
                querydic = eval(request.body)
                if querydic != None and len(querydic) ==4:
                    paramsstatus = querydic.get('status')
                    resourceinfo = querydic.get('resourceinfo')
                    resourcetype = querydic.get('resourcetype')
                    resourceattributes = querydic.get('resourceattributes')
                    if paramsstatus not in ["enable","disable"] or resourceinfo == None or len(resourceinfo)==0 or resourcetype == None or len(resourcetype)==0 or resourceattributes == None or len(resourceattributes)==0:
                        return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST) 
                    if resourcetype == 'vip' and resourceattributes =='id':
                        tb_fact_device_info.objects.filter(id__in=resourceinfo).update(vip_enable_switch=paramsstatus)
                        tb_fact_device_info.objects.filter(id__in=resourceinfo).update(vip_status=paramsstatus) 
                        queryset = tb_fact_device_info.objects.filter(id__in=resourceinfo)
                        serializer = self.get_serializer(queryset,many=True)
                        return Response({'code':1,'msg':serializer.data},status=status.HTTP_200_OK)
                    if resourcetype == 'vip' and resourceattributes =='ip':
                        tb_fact_device_info.objects.filter(vip_address__in=resourceinfo).update(vip_enable_switch=paramsstatus)
                        tb_fact_device_info.objects.filter(vip_address__in=resourceinfo).update(vip_status=paramsstatus) 
                        queryset = tb_fact_device_info.objects.filter(id__in=resourceinfo)
                        serializer = self.get_serializer(queryset,many=True)
                        return Response({'code':1,'msg':serializer.data},status=status.HTTP_200_OK)
                    if resourcetype == 'node':
                        tb_fact_device_info.objects.filter(node_id__in=resourceinfo).update(vip_enable_switch=paramsstatus) 
                        tb_fact_device_info.objects.filter(node_id__in=resourceinfo).update(vip_status=paramsstatus) 
                        queryset = tb_fact_device_info.objects.filter(node_id__in=resourceinfo)
                        serializer = self.get_serializer(queryset,many=True)
                        return Response({'code':1,'msg':serializer.data},status=status.HTTP_200_OK)
                else:
                    return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST) 
        return Response({'code':1,'msg':""},status=status.HTTP_200_OK)

    #资源是否采用探测模块的数据,调整资源状态
    @action(detail=False,methods=['post'])
    def adjust_resource(self,request):
        record_list = []
        try:
            with transaction.atomic():            
                querydic = eval(request.body)
                if querydic != None and len(querydic) ==4:
                    detectstatus = querydic.get('detectstatus')
                    artificialstatus = querydic.get('artificialstatus')
                    resourceinfo = querydic.get('resourceinfo')
                    resourcetype = querydic.get('resourcetype')
                    if detectstatus not in ["enable","disable"] or artificialstatus not in ["enable","disable"] or resourceinfo == None or len(resourceinfo) ==0 or resourcetype == None or len(resourcetype)==0:
                        return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST) 
                    if resourcetype == 'vip':
                        for devid in resourceinfo:
                            tb_fact_device_info.objects.filter(id=devid).update(vip_enable_switch=detectstatus) 
                            tb_fact_device_info.objects.filter(id=devid).update(vip_status=artificialstatus) 
                            queryset = tb_fact_device_info.objects.filter(id=devid)
                            serializer = self.get_serializer(queryset,many=True)
                            record_list.append(serializer.data) 
                        return Response({'code':1,'msg':record_list},status=status.HTTP_200_OK)
                    if resourcetype == 'node':
                        for nodeid in resourceinfo:
                            tb_fact_device_info.objects.filter(node_id=nodeid).update(vip_enable_switch=detectstatus) 
                            tb_fact_device_info.objects.filter(node_id=nodeid).update(vip_status=artificialstatus) 
                            queryset = tb_fact_device_info.objects.filter(node_id=nodeid)
                            serializer = self.get_serializer(queryset,many=True)
                            record_list.append(serializer.data) 
                        return Response({'code':1,'msg':record_list},status=status.HTTP_200_OK)
                else:
                    return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST) 
        return Response({'code':1,'msg':""},status=status.HTTP_200_OK)
   
        #删除资源
    @action(detail=False,methods=['post'])
    def delete_resource(self,request):
        try:
            with transaction.atomic():            
                querydic = eval(request.body)
                if querydic != None and len(querydic) ==3:
                    resourceinfo = querydic.get('resourceinfo')
                    resourcetype = querydic.get('resourcetype')
                    resourceattributes = querydic.get('resourceattributes')
                    if resourceinfo == None or len(resourceinfo) == 0 or resourcetype == None or len(resourcetype) == 0 or resourceattributes == None or len(resourceattributes)==0:
                        return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST)
                    if resourcetype == 'vip' and resourceattributes =='id':
                        tb_fact_device_info.objects.filter(id__in = resourceinfo).delete()   
                        return Response({'code':1,'msg':"del ok"},status=status.HTTP_200_OK)
                    if resourcetype == 'vip' and resourceattributes =='ip':
                        tb_fact_device_info.objects.filter(vip_address__in = resourceinfo).delete()   
                        return Response({'code':1,'msg':"del ok"},status=status.HTTP_200_OK)
                    if resourcetype == 'node':
                        tb_fact_device_info.objects.filter(node_id__in = resourceinfo).delete() 
                        return Response({'code':1,'msg':"del ok"},status=status.HTTP_200_OK)  
                else:
                    return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST) 
        return Response({'code':1,'msg':""},status=status.HTTP_200_OK)
                
                
     
                    
#支持增删改查view
class Viewtypeinfo(MyModelViewSet):
    queryset = tb_fact_viewtype_info.objects.all()
    serializer_class = ViewtypeSerializer
class Viewinfo(MyModelViewSet):
    queryset = tb_fact_temp_view_info.objects.all()
    serializer_class = ViewSerializer
     
    #通过关键字查找item
    @action(detail=False,methods=['get'])
    def get_child_region(self,request):
        try:
            fatherid = request.GET.get('fatherid')
            country = request.GET.get('country', None)
            isp = request.GET.get('isp', None)
            region = request.GET.get('region', None)
            province = request.GET.get('province', None)
            city = request.GET.get('city', None)
            queryset = tb_fact_temp_view_info.objects.all()
            if fatherid != None:
                queryset = queryset.filter(view_father_id = fatherid)
            if country != None:
                queryset = queryset.filter(view_country__contains = country)
            if isp != None:
                queryset = queryset.filter(view_isp__contains=isp)
            if region != None:
                queryset = queryset.filter(view_region__contains=region)
            if province != None:
                queryset = queryset.filter(view_province__contains=province)
            if city != None:
                queryset = queryset.filter(view_city__contains=city)
            serializer = self.serializer_class(queryset,many=True)
            return Response({'code':1,'msg': serializer.data},status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)

#支持增删查改nameid
class Nameidinfo(MyModelViewSet):
    queryset = tb_fact_nameid_info.objects.all()
    def get_serializer_class(self):
        if self.action in ['list','retrieve','universal_matching_nameid','get_all_nameid']:
            return NameidListSerializer
        return NameidUpdateSerializer
       
    @action(detail=False,methods=['get'])
    def push_nameid(self,request):
        try:
            nameid_id = request.GET.get('nameid_id')
            if nameid_id == None or len(nameid_id) == 0:
                return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST)
            tb_fact_nameid_info.objects.filter(id=nameid_id).update(nameid_status="enable")
            return Response({'code':1,'msg':"ok"},status=status.HTTP_200_OK)        
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST) 
    @action(detail=False,methods=['get'])
    def universal_matching_nameid(self,request):
        try:
            nameid = request.GET.get('nameid')
            queryset = tb_fact_nameid_info.objects.all()
            if nameid != None:
                queryset = queryset.filter(nameid_name__contains = nameid) 
            serializer = self.get_serializer(queryset,many=True)
            return Response({'code':1,'msg': serializer.data},status=status.HTTP_200_OK)        
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)        
    @action(detail=False,methods=['get'])
    def get_nameid_from_config(self,request):
        try:
            nameid = request.GET.get('nameid')   
            res = read_from_cache_cluster("vipdevice","nameid-manual",nameid)
            if res: 
                return Response({'code':1,'msg':[res]},status=status.HTTP_200_OK)
            else:
                return Response({'code':0,'msg':str("the nameid is not exixts")},status=status.HTTP_400_BAD_REQUEST)        
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)        
    
    @action(detail=False,methods=['get'])
    def get_nameid_from_qdnsconfig(self,request):  
        try:
            nameid = request.GET.get('nameid')   
            queryset = tb_fact_nameid_info.objects.filter(nameid_name = nameid)
            if queryset and len(queryset) !=0:
                obj = queryset[0]
                if obj:
                    res =  read_from_cache_cluster("vipdevice",str(obj.nameid_policy),nameid)
                    if res != None:
                        return Response({'code':1,'msg':[res]},status=status.HTTP_200_OK)
            return Response({'code':0,'msg':str("the nameid is not exixts")},status=status.HTTP_400_BAD_REQUEST)        
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)        
      
    @action(detail=False,methods=['get'])
    def copy_name(self,request):
        record_list = []
        try:
            nameid = request.GET.get('nameid')
            nameid_id = request.GET.get('nameid_id')
            if nameid == None or len(nameid) == 0 or nameid_id == None or len(nameid_id) == 0:
                return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST)
            with transaction.atomic():
                queryset = tb_fact_nameid_info.objects.filter(id = nameid_id)
                if queryset and len(queryset) != 0:
                    obj = queryset[0]
                    serializer = NameidUpdateSerializer(data={"nameid_name":nameid,"zone_type":obj.zone_type_id,"dns_type":obj.dns_type_id,"nameid_status":obj.nameid_status,"nameid_policy":obj.nameid_policy_id})
                    if not serializer.is_valid():
                        return Response({'code':0,'msg':str(serializer.errors)},status=status.HTTP_400_BAD_REQUEST)
                    serializer.save()
                    res = tb_fact_nameid_info.objects.filter(nameid_name=nameid)
                    newnameidobj = res[0].id
                    querysetview = tb_dimension_nameid_view_info.objects.filter(nameid_id_id=nameid_id) 
                    if querysetview and len(querysetview) != 0:
                        for objview in querysetview:
                            serializer = NameidViewSerializer(data={"nameid_id":newnameidobj,"nameid_view_id":objview.nameid_view_id_id,"nameid_resolve_type":objview.nameid_resolve_type,"nameid_max_ip":objview.nameid_max_ip,"nameid_preferred":objview.nameid_preferred,"nameid_status":objview.nameid_status,"nameid_ttl":objview.nameid_ttl})
                            if not serializer.is_valid():
                                raise serializers.ValidationError
                        querysetviewdev = tb_dimension_nameid_view_device_info.objects.filter(nameid_id_id=nameid_id)
                        if querysetviewdev and len(querysetviewdev) !=0:
                            for objviewdev in querysetviewdev:
                                serializer = NameidViewDeviceSerializer(data={"nameid_id":newnameidobj,"nameid_view_id":objviewdev.nameid_view_id_id,"nameid_device_id":objviewdev.nameid_device_id_id,"nameid_device_ratio":objviewdev.nameid_device_ratio,"nameid_device_status":objviewdev.nameid_device_status})
                                if not serializer.is_valid():
                                    raise serializers.ValidationError
                                else:
                                    record_list.append(serializer.data)
                        querysetviewcname = tb_dimension_nameid_view_cname_info.objects.filter(nameid_id_id=nameid_id)
                        if querysetviewcname and len(querysetviewcname) !=0:
                            for objviewcname in querysetviewcname:
                                serializer = NameidViewCnameSerializer(data={"nameid_id":newnameidobj,"nameid_view_id":objviewcname.nameid_view_id_id,"nameid_cname_id":objviewcname.nameid_cname_id_id,"nameid_cname_ratio":objviewcname.nameid_cname_ratio,"nameid_cname_status":objviewcname.nameid_cname_status})
                                if not serializer.is_valid():
                                    raise serializers.ValidationError
                                else:
                                    record_list.append(serializer.data)
                    else:
                        raise RuntimeError('the nameid view is not exixts')
                else:
                    raise RuntimeError('the nameid is not exixts')
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)
        return Response({'code':1,'msg':record_list},status=status.HTTP_200_OK)

#对域名和view之间的管理
class NameidViewinfo(MyModelViewSet):
    queryset = tb_dimension_nameid_view_info.objects.all()
    serializer_class = NameidViewSerializer
    @action(detail=False,methods=['get'])
    def get_accurate_view_byquery(self,request):
        try:
            nameid = request.GET.get('nameid')
            viewid = request.GET.get('viewid')
            queryset = tb_dimension_nameid_view_info.objects.all()
            if nameid != None:
                queryset = queryset.filter(nameid_id = nameid)
            if viewid != None:
                queryset = queryset.filter(nameid_view_id=viewid)
            serializer = NameidViewListSerializer(queryset,many=True)
            return Response({'code':1,'msg': serializer.data},status=status.HTTP_200_OK)        
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)        
    @action(methods=['delete'],detail=False)
    def delete_relation_resource(self,request):
        try:
            with transaction.atomic():
                nameid = request.GET.get('nameid')
                viewid = request.GET.get('viewid')
                if nameid == None or len(nameid) == 0 or viewid == None or len(viewid) == 0:
                    return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST)
                tb_dimension_nameid_view_info.objects.filter(Q(nameid_id=nameid) & Q(nameid_view_id=viewid)).delete()
                tb_dimension_nameid_view_device_info.objects.filter(Q(nameid_id=nameid) & Q(nameid_view_id=viewid)).delete()
                tb_dimension_nameid_view_cname_info.objects.filter(Q(nameid_id=nameid) & Q(nameid_view_id=viewid)).delete()
                return Response({'code':1,'msg':"del ok"},status=status.HTTP_200_OK)        
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)        
        return Response({'code':1,'msg':""},status=status.HTTP_200_OK)
    @action(detail=False,methods=['get'])
    def get_info_by_nameid(self,request):
        try: 
            nameid = request.GET.get('nameid', None)
            queryset = tb_dimension_nameid_view_info.objects.filter(Q(nameid_id = nameid)) 
            serializer = NameidViewListSerializer(queryset,many=True)
            return Response({'code':1,'msg':serializer.data},status=status.HTTP_200_OK)        
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)        
   
#对域名view,设备之间的管理
class NameidViewDeviceinfo(MyModelViewSet):
    queryset = tb_dimension_nameid_view_device_info.objects.all()
    serializer_class = NameidViewDeviceSerializer  
    #通过nodeid或者ip查找
    @action(detail=False,methods=['get'])
    def get_accurate_by_query(self,request):
        try: 
            nameid = request.GET.get('nameid', None)
            viewid = request.GET.get('viewid', None)
            nodeid = request.GET.get('nodeid', None)
            ip = request.GET.get('ip', None)
            queryset = tb_dimension_nameid_view_device_info.objects.all()
            if nameid != None:
                queryset = queryset.filter(nameid_id = nameid)
            if viewid != None:
                queryset = queryset.filter(nameid_view_id=viewid)
            if nodeid != None:
                queryset = queryset.filter(nameid_device_id__node_id=nodeid)
            if ip != None:
                queryset = queryset.filter(nameid_device_id__vip_address=ip)
            serializer = NameidViewDeviceListSerializer(queryset,many=True)
            return Response({'code':1,'msg': serializer.data},status=status.HTTP_200_OK)        
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)        
    
    #通过nodeid和单台设备删除解析，对于nodeid的华传进来的是一系列的devid
    @action(detail=False,methods=['post'])
    def multiple_delete(self,request):
        try:
            with transaction.atomic():
                querydic = eval(request.body)
                if querydic != None and len(querydic) ==1:
                    idlist = querydic.get('idlist')
                    if idlist == None or len(idlist) == 0:
                         return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST)
                    tb_dimension_nameid_view_device_info.objects.filter(id__in=idlist).delete()
                    return Response({'code':1,'msg':str("del ok")},status=status.HTTP_200_OK)
                else:
                    return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)
        return Response({'code':1,'msg':str("")},status=status.HTTP_200_OK)
      
   
    #文本方式导入ip
    @action(detail=False,methods=['post'])
    def multiple_load_ip(self,request):
        record_list = []
        try:
            with transaction.atomic():
                querydic = eval(request.body)
                if querydic != None and len(querydic) ==3:
                    nameid = querydic.get('nameid')
                    viewid = querydic.get('viewid')
                    ipinfo = querydic.get('ipinfo')
                    if nameid == None or viewid == None or ipinfo == None or len(ipinfo)==0:
                        return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST)
                    queryset = tb_fact_device_info.objects.filter(vip_address__in = ipinfo)
                    for devid in queryset:
                        serializer = NameidViewDeviceSerializer(data={"nameid_id":nameid,"nameid_view_id":viewid,"nameid_device_id":devid.id,"nameid_device_status":"enable","nameid_device_ratio":1})
                        if not serializer.is_valid(raise_exception=False):
                            raise serializers.ValidationError
                        serializer.save()
                        record_list.append(serializer.data)
                    
                    '''
                    queryset = tb_dimension_nameid_view_info.objects.filter(Q(nameid_id=nameid) & Q(nameid_view_id=viewid))
                    if len(queryset) == 0:
                        serializer = NameidViewSerializer(data={'nameid_id':nameid, 'nameid_view_id':viewid, 'nameid_resolve_type': 'a', 'nameid_max_ip': 3, 'nameid_preferred': 'rr', 'nameid_status': 'enable', 'nameid_ttl':120})
                        if not serializer.is_valid():
                            raise serializers.ValidationError
                        serializer.save()
                    '''             
                else:
                    return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)
        return Response({'code':1,'msg':record_list},status=status.HTTP_400_BAD_REQUEST)
    #添加一系列的view
    @action(detail=False,methods=['post'])
    def post_fatherview_devid(self,request):
        record_list = []
        try:
            with transaction.atomic():
                querydic = eval(request.body)
                if querydic != None and len(querydic) == 3:
                    nameid = querydic.get('nameid')
                    view_list = querydic.get('viewidinfo')
                    devid_list = querydic.get('devidinfo')
                    if devid_list == None or nameid == None or view_list == None or len(devid_list) == 0 or len(view_list) == 0:
                        return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST) 
                    for fatherid in view_list:
                        queryset = tb_dimension_nameid_view_info.objects.filter(Q(nameid_id=nameid) & Q(nameid_view_id=fatherid))
                        if len(queryset) == 0:
                            serializer = NameidViewSerializer(data={'nameid_id':nameid, 'nameid_view_id':fatherid, 'nameid_resolve_type': 'a', 'nameid_max_ip': 3, 'nameid_preferred': 'rr', 'nameid_status': 'enable', 'nameid_ttl':120})
                            if not serializer.is_valid():
                                raise serializers.ValidationError
                            serializer.save()
                        for devid in devid_list:
                            queryset = tb_dimension_nameid_view_device_info.objects.filter(Q(nameid_id=nameid) & Q(nameid_view_id=fatherid) & Q(nameid_device_id=devid))
                            if len(queryset) == 0:
                                serializer = NameidViewDeviceSerializer(data={"nameid_id":nameid,"nameid_view_id":fatherid,"nameid_device_id":devid,"nameid_device_status":"enable","nameid_device_ratio":1})
                                if not serializer.is_valid(raise_exception=False):
                                    raise serializers.ValidationError
                                serializer.save()
                                record_list.append(serializer.data)
                else:
                    return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST) 
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)        
        return Response({'code':1,'msg':record_list},status=status.HTTP_200_OK)

    #批量工具入口
    #查看所有的域名view设备详细信息
    @action(detail=False,methods=['get'])
    def get_all_resolve_info(self,request):
        try:
            nameid = request.GET.get('nameid')
            viewid = request.GET.get('viewid')
            ip = request.GET.get('ip') 
            nodeid = request.GET.get('nodeid')
            queryset = tb_dimension_nameid_view_device_info.objects.all() 
            if nameid != None:
                queryset = queryset.filter(nameid_id__nameid_name__contains=nameid)
            if viewid != None:
                queryset = queryset.filter(nameid_view_id=viewid)
            if ip != None:
                queryset = queryset.filter(nameid_device_id__vip_address__contains=ip)
            if nodeid != None:
                queryset = queryset.filter(nameid_device_id__node_id__contains=nodeid)
            serializer = NameidViewDeviceListSerializer(queryset,many=True)
            return Response({'code':1,'msg':serializer.data},status=status.HTTP_200_OK)        
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)        
        
    #批量替换ip
    @action(detail=False,methods=['post'])
    def multiple_replace_ip(self,request):
        record_list = []
        try:
            with transaction.atomic():
                querydic = eval(request.body)
                if querydic != None and len(querydic) ==3:
                    delid = querydic.get('delid')
                    replacedevid = querydic.get('replacedevid')
                    nameidviewid = querydic.get('nameidviewid')
                    if delid == None or len(delid) == 0 or replacedevid == None or len(replacedevid)==0 or nameidviewid == None or len(nameidviewid) == 0:
                        return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST)
                    for item in nameidviewid:
                        nameid = item[0]
                        viewid = item[1]
                        for devid in replacedevid:
                            serializer = NameidViewDeviceSerializer(data={"nameid_id":nameid,"nameid_view_id":viewid,"nameid_device_id":devid,"nameid_device_ratio":1,"nameid_device_status":"enable"})
                            if not serializer.is_valid():
                                raise serializers.ValidationError
                            else:
                                record_list.append(serializer.data)
                    tb_dimension_nameid_view_device_info.objects.filter(id__in=delid).delete()
                else:
                    return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)        
        return Response({'code':1,'msg':record_list},status=status.HTTP_200_OK)
 
    #追加ip
    @action(detail=False,methods=['post'])
    def multiple_append_ip(self,request):
        record_list = []
        try:
            with transaction.atomic():
                querydic = eval(request.body)
                if querydic != None and len(querydic) ==2:
                    replacedevid = querydic.get('appenddevid')
                    nameidviewid = querydic.get('nameidviewid')
                    if replacedevid == None or len(replacedevid) == 0 or nameidviewid == None or len(nameidviewid) == 0:
                        return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST)
                    for item in nameidviewid:
                        nameid = item[0]
                        viewid = item[1]
                        for devid in replacedevid:
                            serializer = NameidViewDeviceSerializer(data={"nameid_id":nameid,"nameid_view_id":viewid,"nameid_device_id":devid,"nameid_device_ratio":1,"nameid_device_status":"enable"})
                            if not serializer.is_valid():
                                raise serializers.ValidationError
                            else:
                                record_list.append(serializer.data)
                else:
                    return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)
        return Response({'code':1,'msg':record_list},status=status.HTTP_200_OK)
    #通过域名id查找域名和设备信息
    @action(detail=False,methods=['get'])
    def get_info_by_nameid(self,request):
        try: 
            nameid = request.GET.get('nameid', None)
            queryset = tb_dimension_nameid_view_device_info.objects.filter(Q(nameid_id = nameid)) 
            serializer = NameidViewDeviceListSerializer(queryset,many=True)
            return Response({'code':1,'msg':serializer.data},status=status.HTTP_200_OK)        
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)        
 
#对cname记录的增删改查
class CnameInfo(MyModelViewSet):
    serializer_class = NameidCnameSerializer
    queryset = tb_fact_cname_info.objects.all() 


    #支持按照操作员厂商以及业务的精准匹配
    @action(detail=False,methods=['get'])
    def get_third_resource_info(self,request):
        try:
            cname = request.GET.get('cname')
            operator = request.GET.get('operator')
            supplier = request.GET.get('supplier')
            bussiness = request.GET.get('bussiness')
            queryset = tb_fact_cname_info.objects.all()
            if cname != None:
                queryset = queryset.filter(nameid_cname__contains=cname)
            if operator != None:
                queryset = queryset.filter(nameid_owner__contains=operator)
            if supplier != None:
                queryset = queryset.filter(nameid_supplier__contains=supplier)
            if bussiness != None:
                queryset = queryset.filter(nameid_business__contains=bussiness)
            serializer = self.get_serializer(queryset,many=True)
            return Response({'code':1,'msg':serializer.data},status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)

#对nameid view cname的管理
class NameidViewCnameinfo(MyModelViewSet):
    serializer_class = NameidViewCnameSerializer
    queryset = tb_dimension_nameid_view_cname_info.objects.all()
    #通过cname查找
    @action(detail=False,methods=['get'])
    def get_accurate_by_query(self,request):
        try:
            nameid = request.GET.get('nameid', None)
            viewid = request.GET.get('viewid', None)
            cname = request.GET.get('cname', None)
            queryset = tb_dimension_nameid_view_cname_info.objects.all()
            if nameid != None:
                queryset = queryset.filter(nameid_id = nameid)
            if viewid != None:
                queryset = queryset.filter(nameid_view_id=viewid)
            if cname != None:
                queryset = queryset.filter(nameid_cname_id__nameid_cname__contains=cname)
            serializer = NameidViewCnameListSerializer(queryset,many=True)
            return Response({'code':1,'msg':serializer.data},status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)
    #添加view
    @action(detail=False,methods=['post'])
    def post_fatherview_cnameid(self,request):
        record_list = []
        try:
            with transaction.atomic():
                querydic = eval(request.body)
                if querydic != None and len(querydic) ==3:
                    nameid = querydic.get('nameid')
                    view_list = querydic.get('viewidinfo') or []
                    cname_list = querydic.get('cnameinfo') or []
                    if cname_list == None or nameid == None or view_list == None or len(cname_list) == 0:
                        return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST)
                #添加viewid
                    for fatherid in view_list:
                        queryset = tb_dimension_nameid_view_info.objects.filter(Q(nameid_id=nameid) & Q(nameid_view_id=fatherid))
                        if len(queryset) == 0:
                            serializer = NameidViewSerializer(data={'nameid_id':nameid, 'nameid_view_id':fatherid, 'nameid_resolve_type': 'a', 'nameid_max_ip': 3, 'nameid_preferred': 'rr','nameid_status': 'enable', 'nameid_ttl':120})
                            if not serializer.is_valid():
                                raise serializers.ValidationError
                            serializer.save()
                        for cnameid in cname_list:
                            queryset = tb_dimension_nameid_view_cname_info.objects.filter(Q(nameid_id=nameid) & Q(nameid_view_id=fatherid) & Q(nameid_cname_id=cnameid))
                            if len(queryset) == 0:
                                serializer = NameidViewCnameSerializer(data={"nameid_id":nameid,"nameid_view_id":fatherid,"nameid_cname_id":cnameid,"nameid_cname_status":"enable","nameid_cname_ratio":1})
                                if not serializer.is_valid(raise_exception=False):
                                    raise serializers.ValidationError
                                serializer.save()
                                record_list.append(serializer.data)
                else:
                    return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)
        return Response({'code':1,'msg':record_list},status=status.HTTP_200_OK) 
    @action(detail=False,methods=['get'])
    def get_info_by_nameid(self,request):
        try: 
            nameid = request.GET.get('nameid', None)
            queryset = tb_dimension_nameid_view_cname_info.objects.filter(Q(nameid_id = nameid)) 
            serializer = NameidViewCnameListSerializer(queryset,many=True)
            return Response({'code':1,'msg':serializer.data},status=status.HTTP_200_OK)        
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)        

#对adminip的管理
class AdminIpInfo(MyModelViewSet):
    queryset = tb_fact_adminip_info.objects.all()
    serializer_class = AdminIpSerializer
  
    @action(detail=False,methods=['get'])
    def get_all_adminip(self,request):
         try:
            nodeid = request.GET.get('nodeid')
            adminip = request.GET.get('adminip')
            isp = request.GET.get('isp')
            region = request.GET.get('region', None)
            province = request.GET.get('province', None)
            queryset = tb_fact_adminip_info.objects.all()
            if nodeid != None:
                queryset = queryset.filter(node_id__contains=nodeid)
            if adminip != None:
                queryset = queryset.filter(admin_ip__contains=ip)
            if isp != None:
                queryset = queryset.filter(isp__contains=isp)
            if region != None:
                queryset = queryset.filter(region__contains=region)
            if province != None:
                queryset = queryset.filter(province__contains=province)
            serializer = self.get_serializer(queryset,many=True)
            return Response({'code':1,'msg':serializer.data},status=status.HTTP_200_OK)
         except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)  

    #修改探针的探测开关
    #要保证把with放到try里面，这样才能保持它的原子性操作
    @action(detail=False,methods=['post'])
    def adjuts_detect_switch(self,request):
        try:
            with transaction.atomic():
                querydic = eval(request.body)
                if querydic != None and len(querydic) ==3:
                    resourceinfo = querydic.get('resourceinfo')
                    switchtype = querydic.get('switchtype')
                    paramstatus = querydic.get('status')
                    if paramstatus not in ["enable","disable"] or resourceinfo == None or len(resourceinfo) == 0 or switchtype == None or len(switchtype) == 0:
                        return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST)
                    if switchtype == "availability":
                        tb_fact_adminip_info.objects.filter(id__in=resourceinfo).update(availability_status=paramstatus)
                        queryset = tb_fact_adminip_info.objects.filter(id__in=resourceinfo)
                        serializer = self.get_serializer(queryset,many=True)
                        return Response({'code':1,'msg':serializer.data},status=status.HTTP_200_OK)
                    if switchtype == "qos":
                        tb_fact_adminip_info.objects.filter(id__in=resourceinfo).update(qos_status=paramstatus)
                        queryset = tb_fact_adminip_info.objects.filter(id__in=resourceinfo)
                        serializer = self.get_serializer(queryset,many=True)
                        return Response({'code':1,'msg':serializer.data},status=status.HTTP_200_OK)
                else:
                    return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)
        return Response({'code':1,'msg':[]},status=status.HTTP_200_OK)
    #删除探针
    @action(detail=False,methods=['post'])
    def delete_detect_resource(self,request):
        try:
            with transaction.atomic():
                querydic = eval(request.body)
                if querydic != None and len(querydic) ==1:
                    resourceinfo = querydic.get('resourceinfo')
                    if resourceinfo == None or len(resourceinfo) == 0:
                        return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST)
                    tb_fact_adminip_info.objects.filter(id__in=resourceinfo).delete()
                    return Response({'code':1,'msg':"del ok"},status=status.HTTP_200_OK)
                else:
                    return Response({'code':0,'msg':"Illegal input"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)
        return Response({'code':1,'msg':""},status=status.HTTP_200_OK)

#对探测任务的管理
class DetectTaskInfo(MyModelViewSet):
    queryset = tb_fact_detecttask_info.objects.all()
    serializer_class = DetectTaskSerializer
    
    @action(detail=False,methods=['get'])    
    def universal_matching_taskname(self,request):
        try:            
            taskname = request.GET.get('taskname')           
            queryset = tb_fact_detecttask_info.objects.all()
            if taskname != None:
                queryset = queryset.filter(detect_name__contains=taskname)
            serializer = self.serializer_class(queryset,many=True)
            return Response({'code':1,'msg': serializer.data},status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)

#对探测数据标准的管理
class DetectDeviceAvailabilityStandardInfo(MyModelViewSet):
    queryset = tb_fact_detectdeviceavailability_standard_info.objects.all()
    serializer_class = DetectDeviceAvailabilityStandardSerializer
    @action(detail=False,methods=['get'])    
    def universal_matching_standard(self,request):
        try:            
            standard = request.GET.get('standard')           
            queryset = tb_fact_detectdeviceavailability_standard_info.objects.all()
            if standard != None:
                queryset = queryset.filter(node_isp__contains=standard)
            serializer = self.serializer_class(queryset,many=True)
            return Response({'code':1,'msg': serializer.data},status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'code':0,'msg':str(err)},status=status.HTTP_400_BAD_REQUEST)
    
#上传设备可用性的源数据
#class DetectDeviceAvailabilityInfo(viewsets.ModelViewSet):
#    queryset = tb_fact_detectdeviceavailability_info.objects.all()
#    serializer_class = DetectDeviceAvailabilitySerializer 
class ShowDetectDeviceAvailabilityInfo(viewsets.ModelViewSet):
    queryset = tb_fact_detectdeviceavailability_info.objects.all()
    serializer_class = DetectDeviceAvailabilitySerializer
#这里对adminip会做检测，但是对 vip先不做检测了，原因在于vip太多，每次上报数据都要查询俩次数据库，没有太多必要,而且没有用到的vip是不会对解析数据造成影响的
class sDetectDeviceAvailabilityInfo(mixins.CreateModelMixin,viewsets.GenericViewSet):
    serializer_class = DetectDeviceAvailabilitySerializer
    def create(self, request, *args, **kwargs):
        try:
            adminip = request.data.get('admin_ip')
            queryset = tb_fact_adminip_info.objects.filter(admin_ip = adminip)
    #        vipdevice = request.data.get('')
            if queryset and len(queryset) != 0:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                 return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response(status=status.HTTP_400_BAD_REQUEST)
class DetectDeviceAvailabilityInfo(ObjectMultipleModelAPIViewSet):
    querylist = [{'queryset':tb_fact_detectdeviceavailability_info, 'serializer_class':DetectDeviceAvailabilitySerializer},{'queryset':tb_fact_detectdeviceavailability_select_info, 'serializer_class':DetectDeviceAvailabilitySelectSerializer},]

#从探测模块下载探测哪些vip数据的接口
from django.http import HttpResponse
from Polaris.detect.get_vipaddress_from_cache import get_vipaddress_from_cache
def url_get_vipaddress_from_cache(request):
    addr = request.GET.get('address','')
    return HttpResponse(get_vipaddress_from_cache(addr))

#dns获取它对应的dnstype
from Polaris.qdns.get_dnstype_from_cache import get_dnstype_from_cache
def url_get_dnstype_from_cache(request):
    dnstype = request.GET.get('address','')
    return HttpResponse(get_dnstype_from_cache(dnstype))

#权威dns获取指定域名对应的数据
from Polaris.qdns.get_nameid_from_cache import get_nameid_from_cache
def url_get_nameid_from_cache(request):
    dnstype = request.GET.get('dnstype','')
    return HttpResponse(get_nameid_from_cache(dnstype))
#获取权威dns对应的zone文件
from Polaris.qdns.get_zone_from_cache import get_zone_from_cache
def url_get_zone_from_cache(request):
    dnstype = request.GET.get('dnstype','')
    return HttpResponse(get_zone_from_cache(dnstype))

#前端获取指定域名的解析信息
