from Polaris.utils.glbscache import read_from_cache_cluster
def get_vipaddress_from_cache(address):
    return read_from_cache_cluster("vipdevice","detect-vipaddress",address) 

