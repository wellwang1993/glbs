from Polaris.utils.glbscache import read_from_cache_cluster
import logging
logger = logging.getLogger('adminip_gettask_access')
import json
def get_vipaddress_from_cache(address):
    logger.info("the adminip {} get task ".format(address))
    res =  read_from_cache_cluster("vipdevice","detect-vipaddress",address) 
    if res== None:
        return ""
    return res
