from django.conf import settings
from django.core.cache import cache
from django_redis import get_redis_connection


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

def read_from_cache_cluster(cluster,key):
    if key == None or cluster == None:
        return None
    conn = get_redis_connection(cluster,con)
    conn.hget(cluster,key) 
def write_to_cache_cluster(cluster,key,value):
    if key == None or cluster == None or con == None or value == None:
        return None
    conn = get_redis_connection(cluster)
    conn.hset(cluster,key,value)
    return 1
