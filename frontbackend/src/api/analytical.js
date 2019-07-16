import request from '@/utils/polaris_request'

export function generateConfig(page) {
  return request({
    url: '/nameid/push_nameid/',
    method: 'get',
    params: page
  })
}
export function copyname(page) {
  return request({
    url: '/nameid/copy_name/',
    method: 'get',
    params: page
  })
}
export function generateView(page) {
  return request({
    url: '/nameidview/push_nameid_viewid/',
    method: 'get',
    params: page
  })
}
export function fetchFatherview(page) {
  return request({
    url: '/view/get_location_info/',
    method: 'get',
    params: page
  })
}
export function fetchSpecialView(page) {
  return request({
    url: '/nameidview/get_accurate_view_byquery_vue/',
    method: 'get',
    params: page
  })
}
export function fetchView(page) {
  return request({
    url: '/nameidview/get_info_by_nameid/',
    method: 'get',
    params: page
  })
}
export function fetchNameidpolicy(page) {
  return request({
    url: '/nameidpolicy/',
    method: 'get'
  })
}
export function fetchDnstype(page) {
  return request({
    url: '/dnstype/',
    method: 'get'
  })
}
export function fetchZone(page) {
  return request({
    url: '/zonetype/',
    method: 'get'
  })
}
export function fetchList(page) {
  return request({
    url: '/nameid/universal_matching_nameid/',
    method: 'get',
    params: page
  })
}
export function fetchIpList(page) {
  return request({
    url: '/vipdevice/get_all_resource_info/',
    method: 'get',
    params: page
  })
}
export function fetchViewIpList(page) {
  return request({
    url: '/nameidviewdevice/get_accurate_by_query/',
    method: 'get',
    params: page
  })
}
export function fetchCnameList(page) {
  return request({
    url: '/cname/get_third_resource_info/',
    method: 'get',
    params: page
  })
}
export function fetchViewCnameList(page) {
  return request({
    url: '/nameidviewcname/get_accurate_by_query/',
    method: 'get',
    params: page
  })
}
export function create(data) {
  return request({
    url: '/nameid/',
    method: 'post',
    data: data
  })
}

export function createview(data) {
  return request({
    url: '/nameidview/',
    method: 'post',
    data: data
  })
}
export function createviewip(data) {
  return request({
    url: '/nameidviewdevice/post_fatherview_devid/',
    method: 'post',
    data: data
  })
}
export function createviewcname(data) {
  return request({
    url: '/nameidviewcname/post_fatherview_cnameid/',
    method: 'post',
    data: data
  })
}
export function update(data, id) {
  return request({
    url: '/nameid/' + id + '/',
    method: 'put',
    data: data,
    query: id
  })
}
export function updateview(data, id) {
  return request({
    url: '/nameidview/' + id + '/',
    method: 'put',
    data: data,
    query: id
  })
}
export function updateviewip(data, id) {
  return request({
    url: '/nameidviewdevice/' + id + '/',
    method: 'put',
    data: data,
    query: id
  })
}
export function updateviewcname(data, id) {
  return request({
    url: '/nameidviewcname/' + id + '/',
    method: 'put',
    data: data,
    query: id
  })
}
export function deleteid(id) {
  return request({
    url: '/nameid/' + id + '/',
    method: 'delete',
    query: id
  })
}
export function sdeleteviewid(id) {
  return request({
    url: '/nameidview/' + id + '/',
    method: 'delete',
    query: id
  })
}
export function deleteviewid(page) {
  return request({
    url: '/nameidview/delete_relation_resource/',
    method: 'delete',
    params: page
  })
}
export function deleteviewipid(id) {
  return request({
    url: '/nameidviewdevice/' + id + '/',
    method: 'delete',
    query: id
  })
}
export function deleteviewcnameid(id) {
  return request({
    url: '/nameidviewcname/' + id + '/',
    method: 'delete',
    query: id
  })
}

