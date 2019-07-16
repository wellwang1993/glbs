from Polaris.utils.glbscache import read_from_cache_cluster,write_to_cache_cluster,delete_to_cache_cluster,get_keys_from_cache
from Polaris.models import tb_fact_nameid_info
import logging
logger = logging.getLogger('qdns_nameid_cluster')
import json

def cluster_nameid_from_cache():
    objs = tb_fact_nameid_info.objects.all()
    dnstype_nameidinfo = {}
    for obj in objs:
        if obj.nameid_status == "enable" and obj.nameid_name is not None and obj.nameid_policy is not None:
            policy = str(obj.nameid_policy)
            nameid_str = read_from_cache_cluster("vipdevice",policy,obj.nameid_name)
            if nameid_str != None:
                nameid_dict = json.loads(nameid_str)
                dnstype = str(obj.dns_type)
                if dnstype_nameidinfo.get(dnstype) == None:
                    dnstype_nameidinfo[dnstype] = {}
                dnstype_nameidinfo[dnstype][obj.nameid_name] = nameid_dict
    keys = get_keys_from_cache("vipdevice","qdns-nameidinfo")
    for key in keys:
        key = str(key,encoding = "raw_unicode_escape")
        if dnstype_nameidinfo.get(key) == None:
            logger.info("the dnstype {} is disable".format(key))
            delete_to_cache_cluster("vipdevice","qdns-nameidinfo",key)
    for dnstype,nameidinfo in dnstype_nameidinfo.items():
        logger.info("the dnstype is {},the nameid info is {}".format(dnstype,json.dumps(nameidinfo)))
        write_to_cache_cluster("vipdevice","qdns-nameidinfo",str(dnstype),json.dumps(nameidinfo))    
