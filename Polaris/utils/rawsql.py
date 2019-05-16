from django.db import connection
import logging
logger = logging.getLogger('default')
def my_custom_sql(sql):
    with connection.cursor() as cursor:
        logger.info(sql)                     
        cursor.execute(sql)  
        raw=cursor.fetchall()  
    return raw
