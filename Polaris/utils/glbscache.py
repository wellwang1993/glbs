from django.conf import settings
from django.core.cache import cache
from django_redis import get_redis_connection
import logging
logger = logging.getLogger('djs')
import json

import json
#read cache user id
def read_from_cache(key):
    if key == None:
        return None
    value = cache.get(key)
    return value

#write cache user id
def write_to_cache(key,value):
    if key == None or value == None:
        return None
    cache.set(key,value,None)
    return 1

def read_from_cache_cluster(con,cluster,key):
    if key == None or cluster == None or con == None:
        return None
    #conn = get_redis_connection(con)
    conn = get_redis_connection("default")
    val = conn.hget(cluster,key) 
    logger.info("@@@@@@@@@@@@@@@@@@@@")
    logger.info(conn.hkeys(cluster))
    logger.info(conn.hvals(cluster))
    logger.info(val)
    if val:
        return str(val,encoding = "utf8")
    return None
def write_to_cache_cluster(con,cluster,key,value):
    if key == None or cluster == None or con == None or value == None:
        return None
    conn = get_redis_connection("default")
    conn.hset(cluster,key,value)
    # conn = get_redis_connection(con)
   # conn.set(cluster,key,value,None)
    return 1
def delete_to_cache_cluster(con,cluster,key):
    if key == None or cluster == None or con == None:
        return None
    conn = get_redis_connection("default")
    conn.hdel(cluster,key)

def flushall_to_cache_cluster(con,cluster):
    conn = get_redis_connection("default")
    conn.flushall(cluster)
