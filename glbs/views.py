# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

from glbs.serializers import DnstypeSerializer,DnszoneSerializer,NameidPolciySerializer,NameidListSerializer,NameidUpdateSerializer,ViewtypeSerializer,ViewSerializer,NameidViewSerializer,NameidViewDeviceSerializer,VipDeviceSerializer,NameidViewDeviceSerializer
from glbs.models import tb_fact_nameid_info,tb_fact_dnszone_info,tb_fact_dnstype_info,tb_fact_nameidpolicy_info,tb_fact_viewtype_info,tb_fact_view_info,tb_dimension_nameid_view_info,tb_dimension_nameid_view_device_info,tb_fact_device_info,tb_dimension_nameid_view_device_info
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.views import APIView
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import Http404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.renderers import JSONRenderer

#支持增删查改dnstype
class Dnstypeinfo(viewsets.ModelViewSet):
    queryset = tb_fact_dnstype_info.objects.all()
    serializer_class = DnstypeSerializer
#支持增删查改zone
class Dnszoneinfo(viewsets.ModelViewSet):
    queryset = tb_fact_dnszone_info.objects.all()
    serializer_class = DnszoneSerializer
#支持增删查改nameid的策略
class NameidPolciyinfo(viewsets.ModelViewSet):
    queryset = tb_fact_nameidpolicy_info.objects.all()
    serializer_class = NameidPolciySerializer
#支持增删查改设备vip
class VipDeviceinfo(viewsets.ModelViewSet):
    queryset = tb_fact_device_info.objects.all()
    serializer_class = VipDeviceSerializer

#支持增删查改nameid
class Nameidinfo(viewsets.ModelViewSet):
    queryset = tb_fact_nameid_info.objects.all()
    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return NameidListSerializer
        return NameidUpdateSerializer
#根据域名获取域名的id
class NameidGetByName(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return NameidListSerializer
        return NameidUpdateSerializer
    def get_queryset(self):
        if self.action in ['retrieve','update','destroy']:
            nameid = self.kwargs.get('nameid', None)
            if nameid is not None:
                queryset = tb_dimension_nameid_view_info.objects.filter(nameid_name = nameid)
            else:
                queryset = tb_fact_nameid_info.objects.all() 
        
        else:
            queryset = tb_fact_nameid_info.objects.all() 
'''
class NameidList(generics.ListCreateAPIView):
    queryset = tb_fact_nameid_info.objects.all()
    serializer_class = NameidSerializer
'''
'''
class NameidDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = tb_fact_nameid_info.objects.all()
    serializer_class = NameidSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)	
'''
'''
class Nameidhh(viewsets.ModelViewSet):
    queryset = tb_fact_nameid_info.objects.all()
    serializer_class = NameidSerializer
'''
class Nameidhh(mixins.CreateModelMixin,\
                   mixins.RetrieveModelMixin,\
                   mixins.UpdateModelMixin,\
                   mixins.DestroyModelMixin,\
                   mixins.ListModelMixin,\
                   viewsets.GenericViewSet):
    queryset = tb_fact_nameid_info.objects.all()
    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return NameidListSerializer
        return NameidUpdateSerializer


class ViewtypeDetail(viewsets.ModelViewSet):
    queryset = tb_fact_viewtype_info.objects.all()
    serializer_class = ViewtypeSerializer
class ViewDetail(viewsets.ModelViewSet):
    queryset = tb_fact_view_info.objects.all()
    serializer_class = ViewSerializer


class NameidViewinfo(viewsets.ModelViewSet):
    queryset = tb_dimension_nameid_view_info.objects.all()
    serializer_class = NameidViewSerializer

class NameidViewDeviceinfo(viewsets.ModelViewSet):
    queryset = tb_dimension_nameid_view_device_info.objects.all()
    serializer_class = NameidViewDeviceSerializer            
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
'''
class testnameid(viewsets.ModelViewSet):
   # queryset = tb_dimension_nameid_view_info.objects.all()
    def get_queryset(self):
        regionid = self.kwargs['id']
        queryset = tb_dimension_nameid_view_info.objects.filter(nameid_view_id_id = regionid)
    serializer_class = NameidViewSerializer
'''
