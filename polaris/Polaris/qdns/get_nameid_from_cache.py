from Polaris.utils.glbscache import read_from_cache_cluster,write_to_cache_cluster
from Polaris.models import tb_fact_nameid_info
import logging
logger = logging.getLogger('qdns_nameid_access')
import json

def get_nameid_from_cache(dnstype):
    logger.info("the {} qdns get nameid ".format(dnstype))
    res = read_from_cache_cluster("vipdevice","qdns-nameidinfo",dnstype)
    if res == None:
        return ""
    return res
