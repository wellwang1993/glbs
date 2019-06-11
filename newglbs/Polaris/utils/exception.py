from rest_framework.response import Response
from rest_framework import status
from django.db import connection, models, transaction
#def ErrorResponse(err_code=errors.SYSTEM_ERROR, err_message='Internal Server Error',
              #message=u'服务器异常', status=status.HTTP_400_BAD_REQUEST, headers=None):

from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['code'] = 0
        response.data['msg'] = response.data['detail']
        #response.data['data'] = None #可以存在
        del response.data['detail'] #删除detail字段

    return response

'''
def set_rollback():
    atomic_requests = connection.settings_dict.get('ATOMIC_REQUESTS', False)
    if atomic_requests and connection.in_atomic_block:
        transaction.set_rollback(True)

def ErrorResponse():
    err = { 
        'error_code': err_code,
        'error': err_message,
        'message': message,
    }   
    return Response(err, status, headers=headers)
class Error(Exception):

    def __init__(self, err_code, err_message='Internal Server Error',
                 message=u'服务器异常', status_code=status.HTTP_400_BAD_REQUEST):
        self.err_code = err_code
        self.err_message = err_message
        self.message = message
        self.status_code = status_code
    def __unicode__(self):
            return u'[Error] %d: %s(%d)' % (self.err_code, self.err_message, self.status_code)
    def getResponse(self):
        return ErrorResponse(self.err_code, self.err_message, self.message, self.status_code)
    
def custom_exception_handler(exc, context):
    if isinstance(exc, Error):
        set_rollback()
        return ErrorResponse(exc.err_code, exc.err_message, exc.message, status=exc.status_code)
    if isinstance(exc, (ForeignObjectRelDeleteError, ModelDontHaveIsActiveFiled)):
        set_rollback()
        return ErrorResponse(errors.PermissionDenied, unicode(exc), u'抱歉, 已有其他数据与之关联, 禁止删除', status=status.HTTP_403_FORBIDDEN)

    if isinstance(exc, (RestPermissionDenied, PermissionDenied)):
        msg = _('Permission denied.')
        data = {
            'detail': six.text_type(msg)
        }
        exc_message = str(exc)
        set_rollback()
        return ErrorResponse(errors.PermissionDenied, data, u'opps, 您没有对应的权限', status=status.HTTP_403_FORBIDDEN)    
        log.error(exc)
'''
