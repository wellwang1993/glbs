from Polaris.models import tb_fact_nameid_info,tb_dimension_nameid_view_info,tb_dimension_nameid_view_device_info,tb_dimension_nameid_view_cname_info,tb_fact_nameid_info
from Polaris.utils.glbscache import read_from_cache_cluster,write_to_cache_cluster,delete_to_cache_cluster
from Polaris.utils.glbscache import read_from_cache,write_to_cache
from Polaris.utils.rawsql import my_custom_sql
import logging
logger = logging.getLogger('policy-detect_device_availability')
import json


def detect_device_availability(multiple_config):
    qdns_res = {}

    if multiple_config != "nameid-default" and multiple_config != "nameid-manual":
        return 
    objs = tb_fact_nameid_info.objects.all()           
    for obj in objs:
        if obj.nameid_name is not None:
            nameid = obj.nameid_name
            status = obj.nameid_status
            policy = str(obj.nameid_policy)
            nameid_obj = read_from_cache_cluster("vipdevice",multiple_config,nameid)
            if nameid_obj != None:
                nameid_obj = json.loads(nameid_obj)
                nameid_obj_replace = {}
                for viewname,viewinfo in nameid_obj.items():
                    if viewinfo != None:
                       nameid_obj_replace[viewname] = {}
                       for k,v in viewinfo.items():
                           if k == "address":
                               nameid_obj_replace[viewname][k] = {}
                               for vip,ratio in v.items():
                                   vipaddress_availability = read_from_cache_cluster("vipdevice","vipaddress-availability",vip)
                                   if vipaddress_availability != None:
                                       if vipaddress_availability == "enable":
                                           nameid_obj_replace[viewname][k][vip] = ratio
                           else:
                               nameid_obj_replace[viewname][k] = v
                       if (nameid_obj_replace[viewname].get("address") == None and nameid_obj_replace[viewname].get("cname") == None) or (nameid_obj_replace[viewname].get("address") != None and len(nameid_obj_replace[viewname]["address"]) == 0 and nameid_obj_replace[viewname].get("cname") != None and len(nameid_obj_replace[viewname]["cname"]) == 0):
                           del nameid_obj_replace[viewname]
                           logger.info("the nameid is {},the view {} is null".format(nameid,viewname))
                if len(nameid_obj_replace) !=0:
                    if qdns_res.get(nameid) == None:
                        qdns_res[nameid] = {}
                    qdns_res[nameid] = nameid_obj_replace
    if multiple_config == "nameid-manual" and len(qdns_res) !=0:
        for nameid,nameidinfo in qdns_res.items():
            write_to_cache_cluster("vipdevice","vipdevice_availability",nameid,json.dumps(nameidinfo)) 

def ssssdetect_device_availability(multiple_config):
    qdns_res = {}
    qdns_res_del = {}

    if multiple_config != "nameid-default" and multiple_config != "nameid-manual":
        return 
    objs = tb_fact_nameid_info.objects.all()           
    for obj in objs:
        if obj.nameid_name is not None:
            nameid = obj.nameid_name
            status = obj.nameid_status
            policy = str(obj.nameid_policy)
            nameid_obj = read_from_cache_cluster("vipdevice",multiple_config,nameid)
            if nameid_obj != None:
                nameid_obj = json.loads(nameid_obj)
                nameid_obj_replace = {}
                for viewname,viewinfo in nameid_obj.items():
                    if viewinfo != None:
                       nameid_obj_replace[viewname] = {}
                       for k,v in viewinfo.items():
                           if k == "address":
                               nameid_obj_replace[viewname][k] = {}
                               for vip,ratio in v.items():
                                   vipaddress_availability = read_from_cache_cluster("vipdevice","vipaddress-availability",vip)
                                   if vipaddress_availability != None:
                                       if vipaddress_availability == "enable":
                                           nameid_obj_replace[viewname][k][vip] = ratio
                           else:
                               nameid_obj_replace[viewname][k] = v
                       if (nameid_obj_replace[viewname].get("address") == None and nameid_obj_replace[viewname].get("cname") == None) or (nameid_obj_replace[viewname].get("address") != None and len(nameid_obj_replace[viewname]["address"]) == 0 and nameid_obj_replace[viewname].get("cname") != None and len(nameid_obj_replace[viewname]["cname"]) == 0):
                           del nameid_obj_replace[viewname]
                           logger.info("the nameid is {},the view {} is null".format(nameid,viewname))
        
                sql = 'select dns_type_id from Polaris_tb_fact_nameid_info where nameid_name = "{}"'.format(nameid)
                res = my_custom_sql(sql) 
                if res != None and len(res) != 0 and multiple_config == "nameid-manual":
                    for item in res:
                        id = item[0]
                        if len(nameid_obj_replace) !=0 and policy == "vipdevice_availability":
                            if qdns_res.get(id)== None:
                                qdns_res[id] = {}
                            qdns_res[id][nameid] = nameid_obj_replace
                        else:
                            if qdns_res_del.get(id) == None:
                                qdns_res_del[id] = {}
                            qdns_res_del[id][nameid] = nameid_obj_replace
    if multiple_config == "nameid-manual" and len(qdns_res) !=0:
        for nameid,nameidinfo in qdns_res.items():
            write_to_cache_cluster("","",)
    for dnstype,nameidinfo in qdns_res.items():
        if multiple_config == "nameid-manual":
            logger.info("the dnstype is {},the nameid info is {}".format(dnstype,json.dumps(nameidinfo)))
            write_to_cache_cluster("vipdevice","policy-device-availability",str(dnstype),json.dumps(nameidinfo))
    if len(qdns_res) == 0:
        for dnstype,nameidinfo in qdns_res_del.items():
            if multiple_config == "nameid-manual":
                logger.info("the dnstype is {},del all nameid {}".format(dnstype,json.dumps(nameidinfo)))
                delete_to_cache_cluster("vipdevice","policy-device-availability",str(dnstype)) 
def sdetect_device_availability(id):
    qdns_res = {}
    qdns_res_del = {}
    objs = tb_fact_nameid_info.objects.all()
    for obj in objs:
        if obj.nameid_name is not None and obj.nameid_policy is not None and obj.nameid_status == 'enable':
            nameid_obj = read_from_cache_cluster("vipdevice","nameid-default",obj.nameid_name)
            logger.info("{}///////////{}".format("====================",nameid_obj))
            if nameid_obj != None:
                nameid_obj = json.loads(nameid_obj)
                nameid_obj_replace = {}
                for viewname,viewinfo in nameid_obj.items():
                    if viewinfo != None:
                       logger.info("innnnnnnnnnnnn")
                       nameid_obj_replace[viewname] = {}
                       for k,v in viewinfo.items():
                           if k == "address":
                               nameid_obj_replace[viewname][k] = {}
                               for vip,ratio in v.items():
                                   logger.info("{}---------{}--------{}".format(vip,ratio,read_from_cache_cluster("vipdevice","vipaddress-availability",vip)))
                                   vipaddress_availability = read_from_cache_cluster("vipdevice","vipaddress-availability",vip)
                                   if vipaddress_availability != None:
                                       if vipaddress_availability == "enable":
                                           nameid_obj_replace[viewname][k][vip] = ratio
                           else:
                               nameid_obj_replace[viewname][k] = v
                       logger.info(len(nameid_obj_replace[viewname]["address"]))
                       logger.info(len(nameid_obj_replace[viewname]["cname"]))
                       if (nameid_obj_replace[viewname].get("address") == None and nameid_obj_replace[viewname].get("cname") == None) or (nameid_obj_replace[viewname].get("address") != None and len(nameid_obj_replace[viewname]["address"]) == 0 and nameid_obj_replace[viewname].get("cname") != None and len(nameid_obj_replace[viewname]["cname"]) == 0):
                           del nameid_obj_replace[viewname]
                           logger.info("DEL!!!!!!!")
                
                sql = 'select dns_type_id from Polaris_tb_fact_nameid_info where nameid_name = "{}"'.format(obj.nameid_name)
                res = my_custom_sql(sql) 
                if res != None and len(res) != 0:
                    for item in res:
                        id = item[0]
                        if len(nameid_obj_replace) !=0:
                            if qdns_res.get(id)== None:
                                qdns_res[id] = {}
                            qdns_res[id][obj.nameid_name] = nameid_obj_replace
                            logger.info("pppppppppp")
                            logger.info("{}++++++++++++++++++++{}".format(obj.nameid_name,json.dumps(nameid_obj_replace)))
                        else:
                            if qdns_res_del.get(id) == None:
                                qdns_res_del[id] = {}
                            qdns_res_del[id][obj.nameid_name] = ""
    for dnstype,nameidinfo in qdns_res.items():
        logger.info("sssssssssssssspppppppppp")
        logger.info("{}++++++++++++++++++++{}".format(type(str(dnstype)),json.dumps(nameidinfo)))
        if multiple_config == "nameid-manual": 
            write_to_cache_cluster("vipdevice","policy-device-availability",str(dnstype),json.dumps(nameidinfo))
    for dnstype,nameidinfo in qdns_res_del.items():
        logger.info("{}____________{}__________{}".format("del",dnstype,json.dumps(nameidinfo)))
        if multiple_config == "nameid-manual": 
            delete_to_cache_cluster("vipdevice","policy-device-availability",str(dnstype)) 
