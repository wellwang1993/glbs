import logging
from Polaris.utils.glbscache import read_from_cache_cluster
logger = logging.getLogger('policy-node_best_qos')
import json
def node_best_qos_policy(nameid,policy):
    logger.info(nameid)
    res = read_from_cache_cluster("vipdevice","vipdevice_availability",nameid)
    logger.info(res)
