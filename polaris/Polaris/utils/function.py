import logging
 
logger = logging.getLogger('dj')
 
 
def print_log(func):  # 定义装饰器
 
    def logs(request):
        return func(request)
 
    return logs


