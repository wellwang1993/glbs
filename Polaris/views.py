# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from Polaris.serializers import DnstypeSerializer,DnszoneSerializer,NameidPolciySerializer,NameidListSerializer,NameidUpdateSerializer,ViewtypeSerializer,ViewSerializer,NameidViewSerializer,NameidViewDeviceSerializer,VipDeviceSerializer,NameidViewDeviceSerializer,NameidViewDeviceListSerializer,NameidViewCnameSerializer,NameidCnameSerializer,NameidViewCnameListSerializer,AdminIpSerializer,DetectTaskSerializer,DetectDeviceAvailabilitySerializer,DetectDeviceAvailabilityStandardSerializer
from Polaris.models import tb_fact_nameid_info,tb_fact_dnszone_info,tb_fact_dnstype_info,tb_fact_nameidpolicy_info,tb_fact_viewtype_info,tb_fact_view_info,tb_dimension_nameid_view_info,tb_dimension_nameid_view_device_info,tb_fact_device_info,tb_dimension_nameid_view_device_info,tb_dimension_nameid_view_cname_info,tb_fact_cname_info,tb_fact_adminip_info,tb_fact_detecttask_info,tb_fact_detectdeviceavailability_info,tb_fact_detectdeviceavailability_standard_info
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.views import APIView
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import Http404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.renderers import JSONRenderer
from django.db.models import Q

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
#        else:
#            queryset = tb_fact_dnstype_info.objects.all()           
        return queryset

#支持增删查改zone
class Dnszoneinfo(viewsets.ModelViewSet):
    queryset = tb_fact_dnszone_info.objects.all()
    serializer_class = DnszoneSerializer
#支持通过zonename查找 item
class GetIdByZone(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = tb_fact_dnszone_info.objects.all()
    serializer_class = DnszoneSerializer
    lookup_field = 'zone_name' 
#   def get_queryset(self):
 #       obj = self.kwargs.get('zonename',None)
 #       if obj is not None:
 #           queryset = tb_fact_dnszone_info.objects.filter(zone_name = obj)
 #       return queryset

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

#支持增删改查view
class Viewtypeinfo(viewsets.ModelViewSet):
    queryset = tb_fact_viewtype_info.objects.all()
    serializer_class = ViewtypeSerializer
class Viewinfo(viewsets.ModelViewSet):
    queryset = tb_fact_view_info.objects.all()
    serializer_class = ViewSerializer

#支持输入father_id输出对应的内容
class GetIdByFatherid(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = ViewSerializer
    def get_queryset(self):
        obj = self.kwargs.get('fatherid', None)
        if obj is not None:
            queryset = tb_fact_view_info.objects.filter(view_father_id = obj)
        else:
            queryset = tb_fact_view_info.objects.all()
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
#对域名和view之间的管理
class NameidViewinfo(viewsets.ModelViewSet):
    queryset = tb_dimension_nameid_view_info.objects.all()
    serializer_class = NameidViewSerializer
#通过域名id和view id获取对应记录id
class GetIdByNameidViewid(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = NameidViewSerializer
    def get_queryset(self):
        nameid = self.kwargs.get('nameid', None)
        viewid = self.kwargs.get('viewid', None)
        if nameid is not None and viewid is not None:
            queryset = tb_dimension_nameid_view_info.objects.filter(Q(nameid_id = nameid) & Q(nameid_view_id=viewid))
        return queryset
#通过域名id删除所有项
class DelByNameid(mixins.DestroyModelMixin,viewsets.GenericViewSet):
    serializer_class = NameidViewSerializer
    lookup_field= 'nameid_id'
    queryset = tb_dimension_nameid_view_info.objects.all() 
    def destroy(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )
        tb_dimension_nameid_view_info.objects.filter(nameid_id=self.kwargs[lookup_url_kwarg]).delete()    
        return Response(status=status.HTTP_204_NO_CONTENT) 

#支持通过域名id查找 item
class GetItemBynameid_inner(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = tb_dimension_nameid_view_info.objects.all()
    serializer_class = NameidViewSerializer
    lookup_field = 'nameid_id' 


#对域名view,设备之间的管理
class NameidViewDeviceinfo(viewsets.ModelViewSet):
    queryset = tb_dimension_nameid_view_device_info.objects.all()
    serializer_class = NameidViewDeviceSerializer            
#通过域名id和view id获取记录
class GetDIdByNameidViewid(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = NameidViewDeviceSerializer
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
    queryset = tb_dimension_nameid_view_device_info.objects.all()
    serializer_class = NameidViewDeviceListSerializer
    lookup_field = 'nameid_id'
#通过域名id删除所有项
class DelDByNameid(mixins.DestroyModelMixin,viewsets.GenericViewSet):
    serializer_class = NameidViewDeviceSerializer
    lookup_field = 'nameid_id'
    queryset = tb_dimension_nameid_view_device_info.objects.all()
    def destroy(self, request, *args, **kwargs):
        queryset =  self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )
        tb_dimension_nameid_view_device_info.objects.filter(nameid_id=self.kwargs[lookup_url_kwarg]).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
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
        else:
            queryset = tb_fact_cname_info.objects.all()           
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
    queryset = tb_dimension_nameid_view_cname_info.objects.all()
    serializer_class = NameidViewCnameListSerializer
    lookup_field = 'nameid_id'

#对adminip的管理
class AdminIpInfo(viewsets.ModelViewSet):
    queryset = tb_fact_adminip_info.objects.all()
    serializer_class = AdminIpSerializer
#对探测任务的管理
class DetectTaskInfo(viewsets.ModelViewSet):
    queryset = tb_fact_detecttask_info.objects.all()
    serializer_class = DetectTaskSerializer 


#def GetRegion(request):
#class GetRegion(viewsets.ModelViewSet):
#    regionid = request.GET.get('id')
#    regioninfo = tb_fact_view_info.objects.filter(view_father_id = regionid)
#    res = []
#    for i in regioninfo:
#        res.append([i.view_id, i.view_name])
#    return render(request, 'region_dropdown_list_options.html',{'regioninfo':res})




class testnameidlist(viewsets.ModelViewSet):
    queryset = tb_dimension_nameid_view_device_info.objects.all()
    serializer_class = NameidViewDeviceSerializer





 #   renderer_classes = [TemplateHTMLRenderer,]
#    template_name = 'tb_dimension_nameid_view_device_info_list.html'
#    def get(self, request, format=None):
#        queryset = tb_dimension_nameid_view_device_info.objects.all()
#        serializers = NameidViewDeviceSerializer(queryset, many=True)
#        return Response({'queryset':queryset})    
#    return Response(serializers.data,template_name ='tb_dimension_nameid_view_device_info_list.html')       
# return Response(serializer.data)
#    def post(self, request, format=None):
#        serializer = NameidViewDeviceSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class testnameidcreate(APIView):
    template_name = 'tb_dimension_nameid_view_device_info_detail.html'

    def get(self, request, pk):
        profile = get_object_or_404(tb_dimension_nameid_view_device_info, pk=pk)
        serializer = NameidViewDeviceSerializer(profile)
        return Response({'serializer': serializer, 'profile': profile})

    def post(self, request, pk):
        profile = get_object_or_404(tb_dimension_nameid_view_device_info, pk=pk)
        serializer = NameidViewDeviceSerializer(profile, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'profile': profile})
        serializer.save()
        return reverse_lazy('tb_dimension_nameid_view_device_info_detail-list')
class testnameidupdate(UpdateView):
    model = tb_dimension_nameid_view_device_info
    success_url = reverse_lazy('person_changelist')

class testsss(viewsets.ModelViewSet):
    queryset = tb_dimension_nameid_view_device_info.objects.all() 
    serializer_class = NameidViewDeviceListSerializer

#上传设备可用性的源数据
class DetectDeviceAvailabilityInfo(viewsets.ModelViewSet):
    queryset = tb_fact_detectdeviceavailability_info.objects.all()
    serializer_class = DetectDeviceAvailabilitySerializer 

#从探测模块下载探测哪些vip数据的接口
from django.http import HttpResponse
from Polaris.detect.get_vipaddress_from_cache import get_vipaddress_from_cache
def url_get_vipaddress_from_cache(request):
    addr = request.GET.get('address','')
    return HttpResponse(get_vipaddress_from_cache(addr))
#权威dns获取指定域名对应的数据
from Polaris.qdns.get_nameid_from_cache import get_nameid_from_cache
def url_get_nameid_from_cache(request):
    dnstype = request.GET.get('dnstype','')
    return HttpResponse(get_nameid_from_cache(dnstype))

class DetectDeviceAvailabilityStandardInfo(viewsets.ModelViewSet):
    queryset = tb_fact_detectdeviceavailability_standard_info.objects.all()
    serializer_class = DetectDeviceAvailabilityStandardSerializer
