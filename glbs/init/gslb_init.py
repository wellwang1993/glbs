# -*- coding: utf-8 -*-
from glbs.models import tb_fact_nameid_info

from glbs.utils.download import urllib_get
from glbs.policy.detect_device_availability_policy import detect_device_availability
from glbs.sync.load_device_availability_cache import load_device_availability_cache

#from glbs.config import config.conf

from glbs.qdns.nameid import ViewClass
from glbs.qdns.nameid import NameidClass




from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


import logging
logger = logging.getLogger('dj')
import json

def serialize_instance(obj):
     d = {}
     d.update(vars(obj))
     return d


#初始化加载nameid
def load_data(url):
    logger.info(url)
    data = urllib_get(url)
    if data is None:
        return
    datastr = str(data,encoding = "utf8")
    obj = json.loads(datastr)
    logger.info(data)
    return obj
@register_job(scheduler, "interval", seconds=10)
def load_confignameid_from_table():
    objs = tb_fact_nameid_info.objects.all()
    for obj in objs:
        if obj.nameid_name is not None and obj.nameid_policy is not None and obj.nameid_status == 'enable':
            url = "{}/{}/".format("http://10.224.10.63:8000/getitembynameid_inner",obj.id)
            nameid_view_data = load_data(url)
            if nameid_view_data is None or nameid_view_data.get("results") is None:
                continue
            obj_list = nameid_view_data["results"]
            nameid_view_dict = {}
            for item in obj_list:
                viewobj = ViewClass().genobj(item)
                nameid_view_dict[item["nameid_view_id"]] = viewobj
            logger.info(nameid_view_dict)
            url = "{}/{}/".format("http://10.224.10.63:8000/getnameinfo",obj.id)
            nameid_device_data = load_data(url)
            if nameid_device_data is None or nameid_device_data.get("results") is None:
                continue
            obj_list = nameid_device_data["results"]
            nameidobj = NameidClass()            
            nameid_name = nameidobj.genobj(obj_list,nameid_view_dict)
            logger.info(json.dumps(nameidobj.nameid_data_dict,default=serialize_instance))   
            logger.info(nameid_name)
#        load_config(obj.id)

#设备可用性策略
@register_job(scheduler, "interval", seconds=10)
def update_nameid_from_disablepolciy():
    objs = tb_fact_nameid_info.objects.all()
    for obj in objs:
        if obj.nameid_name is not None and obj.nameid_policy is not None and obj.nameid_status == 'enable':
            detect_device_availability(obj.id)
#        load_config(obj.id)

#定时加载系统外部数据
@register_job(scheduler, "interval", seconds=10)
def load_extradata_device_availability():
    load_device_availability_cache() 


register_events(scheduler)
