from django.conf import settings
from django.core.cache import cache

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
