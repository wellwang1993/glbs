#-*- coding:UTF-8 -*-
import time
import urllib.request
import urllib.parse
import urllib
import json
import logging
logger = logging.getLogger('default')
def urllib_get(url, timeout_connect=60):

    try:
        resp=urllib.request.urlopen(url,timeout=timeout_connect)
        data = resp.read()
        resp.close()
        return data
    except Exception as err:
        logger.error(err)
        return None

def urllib_post(url,params,timeout_connect=60):
    response = ""
    try:
        data = json.dumps(params)
        jsondataasbytes = data.encode('utf-8') 
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        response = urllib.request.urlopen(req,data=jsondataasbytes)
        response_text = response.read()
        return response_text
    except Exception as err:
        logger.error(err)
        return response
