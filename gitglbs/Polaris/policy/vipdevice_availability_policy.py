from Polaris.models import tb_fact_nameid_info,tb_dimension_nameid_view_info,tb_dimension_nameid_view_device_info,tb_dimension_nameid_view_cname_info,tb_fact_nameid_info
from Polaris.utils.glbscache import read_from_cache_cluster,write_to_cache_cluster,delete_to_cache_cluster,get_keys_from_cache
from Polaris.utils.glbscache import read_from_cache,write_to_cache
from Polaris.utils.rawsql import my_custom_sql
import logging
logger = logging.getLogger('policy-detect_device_availability')
import json
import re

def vipdevice_availability_policy(multiple_config):
    qdns_res = {}
    policy_key = ""
    if multiple_config != "nameid-default" and multiple_config != "nameid-manual":
        return 
    objs = tb_fact_nameid_info.objects.all()           
    for obj in objs:
        if obj.nameid_name is not None:
            try:
                nameid = obj.nameid_name
                status = obj.nameid_status
                policy = str(obj.nameid_policy)
                policy_key = policy
                dnszone = str(obj.zone_type.zone_name)
                if not nameid.endswith(dnszone):
                    logger.info("the nameid {} is  not legal...".format(nameid))
                    continue
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
            except Exception as err:
                logger.error(err) 
                continue
    if policy_key == None:
        policy_key = "vipdevice_availability_policy"
    keys = get_keys_from_cache("vipdevice",policy_key)
    for key in keys:
        key = str(key,encoding = "raw_unicode_escape")
        if qdns_res.get(key) == None:
            logger.info("the nameid {} is disable".format(key))
            delete_to_cache_cluster("vipdevice",policy_key,key)
    for nameid,nameidinfo in qdns_res.items():
        logger.info("the nameid is {},the nameid info is {}".format(nameid,json.dumps(nameidinfo))) 
        write_to_cache_cluster("vipdevice","vipdevice_availability_policy",nameid,json.dumps(nameidinfo)) 

