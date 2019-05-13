from Polaris.utils.glbscache import read_from_cache_cluster
import logging
logger = logging.getLogger('qdns_zone_access')
import json

def get_zone_from_cache(dnstype):
    from django_redis import get_redis_connection
    conn = get_redis_connection("default")

    return read_from_cache_cluster("vipdevice","zone-config",dnstype)
