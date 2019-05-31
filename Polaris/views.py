# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from Polaris.utils.rawsql import my_custom_sql
from Polaris.utils.download import urllib_post,urllib_get
from django.db import IntegrityError, transaction
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from Polaris.serializers import DnstypeSerializer,DnszoneSerializer,NameidPolciySerializer,NameidListSerializer,NameidUpdateSerializer,ViewtypeSerializer,ViewSerializer,NameidViewSerializer,NameidViewDeviceSerializer,VipDeviceSerializer,NameidViewDeviceSerializer,NameidViewDeviceListSerializer,NameidViewCnameSerializer,NameidCnameSerializer,NameidViewCnameListSerializer,AdminIpSerializer,DetectTaskSerializer,DetectDeviceAvailabilitySerializer,DetectDeviceAvailabilityStandardSerializer,DnsIpListSerializer,DnsIpUpdateSerializer,NameidViewListSerializer
from Polaris.models import tb_fact_nameid_info,tb_fact_dnszone_info,tb_fact_dnstype_info,tb_fact_nameidpolicy_info,tb_fact_viewtype_info,tb_dimension_nameid_view_info,tb_dimension_nameid_view_device_info,tb_fact_device_info,tb_dimension_nameid_view_device_info,tb_dimension_nameid_view_cname_info,tb_fact_cname_info,tb_fact_adminip_info,tb_fact_detecttask_info,tb_fact_detectdeviceavailability_info,tb_fact_detectdeviceavailability_standard_info,tb_fact_temp_view_info,tb_fact_dnsip_info
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
#支持增删查改dnstype
class Dnstypeinfo(viewsets.ModelViewSet):
    queryset = tb_fact_dnstype_info.objects.all()
    serializer_class = DnstypeSerializer
#通过dnsname查找item
class GetIdByDnsname(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = DnstypeSerializer
    def get_queryset(self):
        obj = self.kwargs.get('dnsname', None)
        if obj is not None:
            queryset = tb_fact_dnstype_info.objects.filter(dns_name = obj)
        return queryset
#支持增删查改dnsip
class DnsIpinfo(viewsets.ModelViewSet):
    queryset = tb_fact_dnsip_info.objects.all()
    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return DnsIpListSerializer
        return DnsIpUpdateSerializer
#通过dnsip查找item
class GetIdByDnsip(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = DnsIpListSerializer
    def get_queryset(self):
        obj = self.kwargs.get('dnsip', None)
        if obj is not None:
            queryset = tb_fact_dnsip_info.objects.filter(dns_ip = obj)
        return queryset

#支持增删查改zone
class Dnszoneinfo(viewsets.ModelViewSet):
    queryset = tb_fact_dnszone_info.objects.all()
    serializer_class = DnszoneSerializer
#支持通过zonename查找 item
class GetIdByZone(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = DnszoneSerializer
    def get_queryset(self):
        obj = self.kwargs.get('zonename',None)
        if obj is not None:
            queryset = tb_fact_dnszone_info.objects.filter(zone_name = obj)
        return queryset
#支持增删查改nameid的策略
class NameidPolciyinfo(viewsets.ModelViewSet):
    queryset = tb_fact_nameidpolicy_info.objects.all()
    serializer_class = NameidPolciySerializer
#支持通过策略查找item
class GetIdByPolicy(viewsets.ModelViewSet):
    serializer_class = NameidPolciySerializer
    def get_queryset(self):
        obj = self.kwargs.get('policyname',None)
        if obj is not None:
            queryset = tb_fact_nameidpolicy_info.objects.filter(policy_name = obj)
        return queryset

#支持增删查改设备vip
class VipDeviceinfo(viewsets.ModelViewSet):
    queryset = tb_fact_device_info.objects.all()
    serializer_class = VipDeviceSerializer

#根据设备名字查找设备对应的id
class GetIdByVipdev(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = VipDeviceSerializer
    def get_queryset(self):
        obj = self.kwargs.get('vipname', None)
        if obj is not None:
            queryset = tb_fact_device_info.objects.filter(vip_address = obj)
        return queryset
#根据节点id查找内容
class GetIdByNodeName(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = VipDeviceSerializer
    def get_queryset(self):
        obj = self.kwargs.get('nodename', None)
        if obj is not None:
            queryset = tb_fact_device_info.objects.filter(node_id = obj)
        return queryset


class UpdateDevByNodeid(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = VipDeviceSerializer
    def get_queryset(self):
        nodeid = self.kwargs.get('nodeid', None)
        status = self.kwargs.get('status', None)
        if nodeid is not None and status is not None:
            if status == "enable":
                tb_fact_device_info.objects.filter(node_id=nodeid).update(vip_enable_switch='enable') 
                tb_fact_device_info.objects.filter(node_id=nodeid).update(vip_status='enable') 
            if status == "disable":
                tb_fact_device_info.objects.filter(node_id=nodeid).update(vip_enable_switch='disable') 
                tb_fact_device_info.objects.filter(node_id=nodeid).update(vip_status='disable') 
            queryset = tb_fact_device_info.objects.filter(node_id=nodeid)
            return queryset
#支持增删改查view
class Viewtypeinfo(viewsets.ModelViewSet):
    queryset = tb_fact_viewtype_info.objects.all()
    serializer_class = ViewtypeSerializer
class Viewinfo(viewsets.ModelViewSet):
    queryset = tb_fact_temp_view_info.objects.all()
    serializer_class = ViewSerializer

#支持输入father_id输出对应的内容
class GetIdByFatherid(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = ViewSerializer
    def get_queryset(self):
        obj = self.kwargs.get('fatherid', None)
        if obj is not None:
            queryset = tb_fact_temp_view_info.objects.filter(view_father_id = obj)
        return queryset
#为了前期更好的查询，提供的该接口，即输入view对应的中文名字输出对应的view_id
class GetIdByViewInfo(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = ViewSerializer
    def get_queryset(self):
        country = self.kwargs.get('country', None)
        isp = self.kwargs.get('isp', None)
        region = self.kwargs.get('region', None)
        province = self.kwargs.get('province', None)
        city = self.kwargs.get('city', None)
        queryset = tb_fact_temp_view_info.objects.filter(Q(view_country__contains = country) & Q(view_isp__contains=isp) & Q(view_region__contains=region) & Q(view_province__contains=province) & Q(view_city__contains=city))
        return queryset

#支持增删查改nameid
class Nameidinfo(viewsets.ModelViewSet):
    queryset = tb_fact_nameid_info.objects.all()
    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return NameidListSerializer
        return NameidUpdateSerializer
#根据域名获取域名的id
class NameidGetByName(mixins.ListModelMixin,viewsets.GenericViewSet):
    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return NameidListSerializer
        return NameidUpdateSerializer
    def get_queryset(self):
        nameid = self.kwargs.get('nameid', None)
        if nameid is not None:
            queryset = tb_fact_nameid_info.objects.filter(nameid_name = nameid)
        return queryset
#根据域名匹配泛域名
class NameidGetByNameBlurry(mixins.ListModelMixin,viewsets.GenericViewSet):
    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return NameidListSerializer
        return NameidUpdateSerializer
    def get_queryset(self):
        nameid = self.kwargs.get('nameid', None)
        if nameid is not None:
            queryset = tb_fact_nameid_info.objects.filter(nameid_name__contains = nameid)
        return queryset
   
from django.db import IntegrityError, transaction 
def CopyName(request):
    try:
        nameid = request.GET.get('nameid')
        nameid_id = request.GET.get('nameid_id')
        with transaction.atomic():
            queryset = tb_fact_nameid_info.objects.filter(id = nameid_id)
            if queryset and len(queryset) != 0:
                obj = queryset[0]
                newnameobj = tb_fact_nameid_info.objects.create(nameid_name=nameid,zone_type=obj.zone_type,dns_type=obj.dns_type,nameid_status=obj.nameid_status,nameid_policy=obj.nameid_policy)
                
                querysetview = tb_dimension_nameid_view_info.objects.filter(nameid_id_id=nameid_id) 
                if querysetview and len(querysetview) != 0:
                    for objview in querysetview:
                        print(objview)
                        tb_dimension_nameid_view_info.objects.create(nameid_id=newnameobj,nameid_view_id=objview.nameid_view_id,nameid_resolve_type=objview.nameid_resolve_type,nameid_max_ip=objview.nameid_max_ip,nameid_preferred=objview.nameid_preferred,nameid_status=objview.nameid_status,nameid_ttl=objview.nameid_ttl)
                    querysetviewdev = tb_dimension_nameid_view_device_info.objects.filter(nameid_id_id=nameid_id)
                    if querysetviewdev and len(querysetviewdev) !=0:
                        for objviewdev in querysetviewdev:
                            tb_dimension_nameid_view_device_info.objects.create(nameid_id=newnameobj,nameid_view_id=objviewdev.nameid_view_id,nameid_device_id=objviewdev.nameid_device_id,nameid_device_ratio=objviewdev.nameid_device_ratio,nameid_device_status=objviewdev.nameid_device_status)
                    querysetviewcname = tb_dimension_nameid_view_cname_info.objects.filter(nameid_id_id=nameid_id)
                    if querysetviewcname and len(querysetviewcname) !=0:
                        for objviewcname in querysetviewcname:
                            tb_dimension_nameid_view_cname_info.objects.create(nameid_id=newnameobj,nameid_view_id=objviewcname.nameid_view_id,nameid_cname_id=objviewcname.nameid_cname_id,nameid_cname_ratio=objviewcname.nameid_cname_ratio,nameid_cname_status=objviewcname.nameid_cname_status)
                return HttpResponse(status=status.HTTP_201_CREATED)
    except Exception as err:
        print(err)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

from Polaris.utils.glbscache import read_from_cache_cluster,get_keys_from_cache
#通过域名获取运维配置的解析
def url_get_nameidconfig(request):
    nameid = request.GET.get('nameid','')    
    return HttpResponse(read_from_cache_cluster("vipdevice","nameid-manual",nameid))

#通过域名获取经过策略调整后的解析
def url_get_nameidqdnsconfig(request):
    nameid = request.GET.get('nameid','')    
    queryset = tb_fact_nameid_info.objects.filter(nameid_name = nameid)
    
    if queryset and len(queryset) !=0:
        obj = queryset[0]
        if obj:
            res =  read_from_cache_cluster("vipdevice",str(obj.nameid_policy),nameid)
            if res == None:
                return HttpResponse("")
            else:
                return HttpResponse(res)
    return HttpResponse("")


#对域名和view之间的管理
class NameidViewinfo(viewsets.ModelViewSet):
    queryset = tb_dimension_nameid_view_info.objects.all()
    serializer_class = NameidViewSerializer
#通过域名id和view id获取对应记录id
class GetIdByNameidViewid(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = NameidViewListSerializer
    def get_queryset(self):
        nameid = self.kwargs.get('nameid', None)
        viewid = self.kwargs.get('viewid', None)
        if nameid is not None and viewid is not None:
            queryset = tb_dimension_nameid_view_info.objects.filter(Q(nameid_id = nameid) & Q(nameid_view_id=viewid))
        return queryset
#支持通过域名id查找 item
class GetItemBynameid_inner(mixins.ListModelMixin,viewsets.GenericViewSet):
   # queryset = tb_dimension_nameid_view_info.objects.all()
    serializer_class = NameidViewSerializer
   # lookup_field = 'nameid_id' 
    def get_queryset(self):
        nameid = self.kwargs.get('nameid', None)
        if nameid is not None:
            queryset = tb_dimension_nameid_view_info.objects.filter(Q(nameid_id = nameid))
        return queryset
#支持通过域名id查找具体的view信息
class url_GetItemBynameid_inner(mixins.ListModelMixin,viewsets.GenericViewSet):
   # queryset = tb_dimension_nameid_view_info.objects.all()
    serializer_class = NameidViewListSerializer
   # lookup_field = 'nameid_id' 
    def get_queryset(self):
        nameid = self.kwargs.get('nameid', None)
        if nameid is not None:
            queryset = tb_dimension_nameid_view_info.objects.filter(Q(nameid_id = nameid))
        return queryset

#对域名view,设备之间的管理
class NameidViewDeviceinfo(viewsets.ModelViewSet):
    queryset = tb_dimension_nameid_view_device_info.objects.all()
    serializer_class = NameidViewDeviceSerializer            
#添加一系列view
def NameidViewListDeviceinfo(request):
    try:
        with transaction.atomic():
            querydic = eval(request.body)
            if querydic != None and len(querydic) !=0:
                res_list = []
        #print(data)
                nameid = querydic.get('nameid_id')
                viewid = querydic.get('nameid_view_id')
                devid = querydic.get('devid')
               
                #这里有待考虑，添加view以后,查出本view的元信息
                viewinfourl = "http://127.0.0.1:8000/getidbynameview/{}/{}/".format(nameid,viewid)
                viewinfores = urllib_get(viewinfourl)
                if viewinfores == None:
                    return HttpResponse(" ") 
                viewinfodic = json.loads(viewinfores)
                if viewinfodic.get("results") == None:
                    return HttpResponse(" ") 
                viewinfodic = viewinfodic["results"][0]
                print(viewinfodic)
                #将本设备信息插入直接的name view device表中
                data={"nameid_id":nameid,"nameid_view_id":viewid,"nameid_device_id":devid,"nameid_device_status":"enable","nameid_device_ratio":30}
                url = "http://127.0.0.1:8000/nameidviewdevice/"
                res = urllib_post(url,data)
                res_list.append(res)
                #将本设备插入它的父级view中
                view_fatherid = querydic.get('viewfatherid')
                if view_fatherid != None:
                    for fatherid in view_fatherid:
                        #将设备插入父级的name view device表中
                        data["nameid_view_id"] = fatherid
                        res = urllib_post(url,data)
                        res_list.append(res)
                        #将父级的view插入本域名的nameid view信息表中
                        viewurl = "http://127.0.0.1:8000/nameidview/"
                        viewdata = {"nameid_id":nameid,"nameid_view_id":fatherid,"nameid_resolve_type":viewinfodic.get("nameid_resolve_type"),"nameid_max_ip":viewinfodic.get("nameid_max_ip"),"nameid_preferred":viewinfodic.get("nameid_preferred"),"nameid_status":"enable","nameid_ttl":viewinfodic.get("nameid_ttl")}
                        print(viewdata)
                        viewres = urllib_post(viewurl,viewdata)
            return HttpResponse(res_list)  
    except Exception as err:
        print(err)  
    
#通过设备nodeid添加记录
import json
def NameidViewNodeidinfo(request):
    try:
        with transaction.atomic():
            querydic = eval(request.body)
            if querydic != None and len(querydic) !=0:
                nameid = querydic.get('nameid_id')
                viewid = querydic.get('nameid_view_id')
                nodeid = querydic.get('nodeid')
                viewinfourl = "http://127.0.0.1:8000/getidbynameview/{}/{}/".format(nameid,viewid)
                viewinfores = urllib_get(viewinfourl)
                if viewinfores == None:
                    return HttpResponse(" ")
                viewinfodic = json.loads(viewinfores)
                if viewinfodic.get("results") == None:
                    return HttpResponse(" ")
                viewinfodic = viewinfodic["results"][0]

                record_list = []
                 
                queryset = tb_fact_device_info.objects.filter(node_id=nodeid)
                print(queryset)
                url = "http://127.0.0.1:8000/nameidviewdevice/"
                if queryset != None and len(queryset) != 0:
           
                    for obj in queryset:
                        data = {"nameid_id":nameid,"nameid_view_id":viewid,"nameid_device_id":obj.id,"nameid_device_status":"enable","nameid_device_ratio":30}
                        print(data)
                        res = urllib_post(url,data)
                        record_list.append(res)
                    view_fatherid = querydic.get('viewfatherid')
                    if view_fatherid != None:
                        for fatherid in view_fatherid:
                            for obj in queryset:
                                data = {"nameid_id":nameid,"nameid_view_id":fatherid,"nameid_device_id":obj.id,"nameid_device_status":"enable","nameid_device_ratio":30}
                                print(data)
                                res = urllib_post(url,data)
                                record_list.append(res)

                                viewurl = "http://127.0.0.1:8000/nameidview/"
                                viewdata = {"nameid_id":nameid,"nameid_view_id":fatherid,"nameid_resolve_type":viewinfodic.get("nameid_resolve_type"),"nameid_max_ip":viewinfodic.get("nameid_max_ip"),"nameid_preferred":viewinfodic.get("nameid_preferred"),"nameid_status":"enable","nameid_ttl":viewinfodic.get("nameid_ttl")}
                                print(viewdata)
                                viewres = urllib_post(viewurl,viewdata)
                        
    except Exception as err:
        print(err)
    return HttpResponse(record_list)    
#批量添加ip


#通过域名id和view id获取记录
class GetDIdByNameidViewid(mixins.ListModelMixin,viewsets.GenericViewSet):
    #serializer_class = NameidViewDeviceSerializer
    serializer_class = NameidViewDeviceListSerializer
    def get_queryset(self):
        nameid = self.kwargs.get('nameid', None)
        viewid = self.kwargs.get('viewid', None)
        if nameid is not None and viewid is not None:
            queryset = tb_dimension_nameid_view_device_info.objects.filter(Q(nameid_id = nameid) & Q(nameid_view_id=viewid))
        return queryset
#通过域名id和view id和设备id获取记录
class GetIdByNameidViewidDeviceid(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = NameidViewDeviceSerializer
    def get_queryset(self):
        nameid = self.kwargs.get('nameid', None)
        viewid = self.kwargs.get('viewid', None)
        deviceid = self.kwargs.get('deviceid', None)
        if nameid is not None and viewid is not None and deviceid is not None:
            queryset = tb_dimension_nameid_view_device_info.objects.filter(Q(nameid_id = nameid) & Q(nameid_view_id=viewid) & Q(nameid_device_id = deviceid))
        return queryset
#通过域名id查找域名和设备信息
class GetNameDevInfoByNameid(mixins.ListModelMixin,viewsets.GenericViewSet):
#    queryset = tb_dimension_nameid_view_device_info.objects.all()
    serializer_class = NameidViewDeviceListSerializer
    def get_queryset(self):
        nameid = self.kwargs.get('nameid', None)
        if nameid is not None:
            queryset = tb_dimension_nameid_view_device_info.objects.filter(Q(nameid_id = nameid))
        return queryset
#对cname记录的增删改查
class CnameInfo(viewsets.ModelViewSet):
    serializer_class = NameidCnameSerializer
    queryset = tb_fact_cname_info.objects.all() 
#支持按照操作员厂商以及业务的精准匹配
class GetItemByOpSuBu(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = NameidCnameSerializer
    def get_queryset(self):
        operator = self.kwargs.get('operator', None)
        supplier = self.kwargs.get('supplier', None)
        bussiness = self.kwargs.get('bussiness', None)
        if operator is not None and supplier is not None and bussiness is not None:
            queryset = tb_fact_cname_info.objects.filter(Q(nameid_owner=operator) & Q(nameid_supplier=supplier) & Q(nameid_business=bussiness))
        return queryset
#支持按照域名模糊匹配

#对nameid view cname的管理
class NameidViewCnameinfo(viewsets.ModelViewSet):
    serializer_class = NameidViewCnameSerializer
    queryset = tb_dimension_nameid_view_cname_info.objects.all()

#通过域名id和view id获取记录
class GetCIdByNameidViewid(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = NameidViewCnameSerializer
    def get_queryset(self):
        nameid = self.kwargs.get('nameid', None)
        viewid = self.kwargs.get('viewid', None)
        if nameid is not None and viewid is not None:
            queryset = tb_dimension_nameid_view_cname_info.objects.filter(Q(nameid_id = nameid) & Q(nameid_view_id=viewid))
        return queryset
#通过域名 id.view id cname id查找对应的记录
class GetCIdByNameidViewidCnameid(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = NameidViewCnameSerializer
    def get_queryset(self):
        nameid = self.kwargs.get('nameid', None)
        viewid = self.kwargs.get('viewid', None)
        cnameid = self.kwargs.get('cnameid', None)
        if nameid is not None and viewid is not None and cnameid is not None:
            queryset = tb_dimension_nameid_view_cname_info.objects.filter(Q(nameid_id = nameid) & Q(nameid_view_id=viewid) & Q(nameid_cname_id = cnameid))
        return queryset
#通过域名查找配置的cname信息
class GetNameCnameInfoByNameid(mixins.ListModelMixin,viewsets.GenericViewSet):
    #queryset = tb_dimension_nameid_view_cname_info.objects.all()
    serializer_class = NameidViewCnameListSerializer
    #lookup_field = 'nameid_id'
    def get_queryset(self):
        nameid = self.kwargs.get('nameid', None)
        if nameid is not None:
            queryset = tb_dimension_nameid_view_cname_info.objects.filter(Q(nameid_id = nameid))
        return queryset

#对adminip的管理
class AdminIpInfo(viewsets.ModelViewSet):
    queryset = tb_fact_adminip_info.objects.all()
    serializer_class = AdminIpSerializer
class GetAdminIdByViewInfo(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = AdminIpSerializer
    def get_queryset(self):
        isp = self.kwargs.get('isp', None)
        region = self.kwargs.get('region', None)
        province = self.kwargs.get('province', None)
        queryset = tb_fact_adminip_info.objects.filter(Q(isp__contains=isp) & Q(region__contains=region) & Q(province__contains=province))
        return queryset

#对探测任务的管理
class DetectTaskInfo(viewsets.ModelViewSet):
    queryset = tb_fact_detecttask_info.objects.all()
    serializer_class = DetectTaskSerializer
#通过探测任务查找id 
class GetIdByTaskInfo(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = DetectTaskSerializer
    def get_queryset(self):
        taskname = self.kwargs.get('taskname', None)
        queryset = tb_fact_detecttask_info.objects.filter(detect_name=taskname)
        return queryset

#对探测数据标准的管理
class DetectDeviceAvailabilityStandardInfo(viewsets.ModelViewSet):
    queryset = tb_fact_detectdeviceavailability_standard_info.objects.all()
    serializer_class = DetectDeviceAvailabilityStandardSerializer

#通过运营商查找id 
class GetIdByStandardInfo(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = DetectDeviceAvailabilityStandardSerializer
    def get_queryset(self):
        standard = self.kwargs.get('standard', None)
        queryset = tb_fact_detectdeviceavailability_standard_info.objects.filter(node_isp=standard)
        return queryset
#上传设备可用性的源数据
#class DetectDeviceAvailabilityInfo(viewsets.ModelViewSet):
#    queryset = tb_fact_detectdeviceavailability_info.objects.all()
#    serializer_class = DetectDeviceAvailabilitySerializer 
class ShowDetectDeviceAvailabilityInfo(viewsets.ModelViewSet):
    queryset = tb_fact_detectdeviceavailability_info.objects.all()
    serializer_class = DetectDeviceAvailabilitySerializer
#这里对adminip会做检测，但是对 vip先不做检测了，原因在于vip太多，每次上报数据都要查询俩次数据库，没有太多必要,而且没有用到的vip是不会对解析数据造成影响的
class DetectDeviceAvailabilityInfo(mixins.CreateModelMixin,viewsets.GenericViewSet):
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
