#-*- coding:UTF-8 -*-
import time
import urllib.request
import logging
logger = logging.getLogger('dj')
def urllib_get(url, timeout_connect=60):

    try:
        resp=urllib.request.urlopen(url,timeout=timeout_connect)
        data = resp.read()
        resp.close()
        return data
    except Exception as err:
        return None

