from Polaris.utils.glbscache import read_from_cache_cluster
import logging
logger = logging.getLogger('dj')
import json

def get_nameid_from_cache(dnstype):
    logger.info(type(dnstype))
    logger.info("%%%%%%%%%%%%")
    logger.info(json.dumps(read_from_cache_cluster("vipdevice","policy-device-availability",dnstype)))
    from django_redis import get_redis_connection
    conn = get_redis_connection("default")
    logger.info(json.dumps(conn.hkeys("default")))
    logger.info(json.dumps(conn.hvals("default")))
    
    return read_from_cache_cluster("vipdevice","policy-device-availability",dnstype)

