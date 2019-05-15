from Polaris.utils.glbscache import read_from_cache_cluster
import logging
logger = logging.getLogger('qdns_zone_access')
import json

def get_zone_from_cache(dnstype):
    logger.info("the {} get zone ".format(dnstype))
    return read_from_cache_cluster("vipdevice","zone-config",dnstype)
