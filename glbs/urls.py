from django.urls import path,include
from glbs import views

from glbs.views import Nameidhh
snippet_detail = Nameidhh.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
snippet_list = Nameidhh.as_view({
    'get': 'list',
    'post': 'create'
})

'''
urlpatterns = [
    path('dnszone/', views.DnszoneList.as_view()),
    path('dnstype/', views.DnstypeList.as_view()),
    
    path('nameid/', snippet_list),
    path('nameidpolicy/', views.NameidPolciyList.as_view()),
    path('nameiddetail/<int:pk>/',snippet_detail),
    
]
'''
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register(r'dnstype',views.Dnstypeinfo)
router.register(r'dnszone',views.Dnszoneinfo)
router.register(r'nameidpolicy',views.NameidPolciyinfo)
router.register(r'vipdevice',views.VipDeviceinfo)
router.register(r'nameid', views.Nameidinfo)

#通过域名获取域名id
#router.register(r'getbyname/(?P<nameid>.+)',views.NameidGetByName,base_name='nameid')
router.register(r'getbyname)',views.NameidGetByName,base_name='nameid')


router.register(r'viewtype',views.ViewtypeDetail)
router.register(r'view',views.ViewDetail)
router.register(r'nameidview',views.NameidViewinfo)
router.register(r'nameidviewdevice',views.NameidViewDeviceinfo)

#router.register(r'view/(?P<id>[0-9]+)',views.ViewDetail,base_name='nameid')
#router.register(r'nameidview/(?P<id>[0-9]+)',views.NameidViewDetail)
router.register(r'testnameidlist',views.testnameidlist)

urlpatterns = [
#    path('testnameidlist/',views.testnameidlist.as_view(),name = 'testnameidlist'),
    path('testnameidcreate/<int:pk>',views.testnameidcreate.as_view()),
   # path('ajax/GetRegion',views.GetRegion, name='ajax_GetRegion'),
    path('', include(router.urls)),
]
