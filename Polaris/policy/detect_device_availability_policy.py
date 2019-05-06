from Polaris.models import tb_fact_nameid_info,tb_dimension_nameid_view_info,tb_dimension_nameid_view_device_info,tb_dimension_nameid_view_cname_info
from Polaris.utils.glbscache import read_from_cache_cluster,write_to_cache_cluster
from Polaris.utils.glbscache import read_from_cache,write_to_cache
from Polaris.utils.rawsql import my_custom_sql
import logging
logger = logging.getLogger('dj')
import json

def detect_device_availability(id):
    qdns_res = {}
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
                if len(nameid_obj_replace) != 0:
                    sql = 'select dns_type_id from Polaris_tb_fact_nameid_info where nameid_name = "{}"'.format(obj.nameid_name)
                    res = my_custom_sql(sql) 
                    for item in res:
                        id = item[0]
                        if qdns_res.get(id)== None:
                            qdns_res[id] = {}
                        qdns_res[id][obj.nameid_name] = nameid_obj_replace
                   # write_to_cache_cluster("vipdevice","policy-device-availability",obj.nameid_name,json.dumps(nameid_obj_replace))
                        logger.info("pppppppppp")
                        logger.info("{}++++++++++++++++++++{}".format(obj.nameid_name,json.dumps(nameid_obj_replace)))
                else:
                    logger.info("pppppppppp==============================")
    for dnstype,nameidinfo in qdns_res.items():
        logger.info("sssssssssssssspppppppppp")
        logger.info("{}++++++++++++++++++++{}".format(type(str(dnstype)),json.dumps(nameidinfo)))
        write_to_cache_cluster("vipdevice","policy-device-availability",str(dnstype),json.dumps(nameidinfo))
           
