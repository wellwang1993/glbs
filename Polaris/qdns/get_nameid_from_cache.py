from Polaris.utils.glbscache import read_from_cache_cluster
import logging
logger = logging.getLogger('dj')
import json

def get_nameid_from_cache(dnstype):
    logger.info(type(dnstype))
    logger.info("%%%%%%%%%%%%")
    return read_from_cache_cluster("vipdevice","policy-device-availability",dnstype)

