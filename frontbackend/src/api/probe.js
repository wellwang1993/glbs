import request from '@/utils/polaris_request'

export function fetchList(page) {
  return request({
    url: '/adminip/get_all_adminip/',
    method: 'get',
    params: page
  })
}
export function create(data) {
  return request({
    url: '/adminip/',
    method: 'post',
    data: data
  })
}
export function update(data, id) {
  return request({
    url: '/adminip/' + id + '/',
    method: 'put',
    data: data,
    query: id
  })
}
export function deleteid(id) {
  return request({
    url: '/adminip/' + id + '/',
    method: 'delete',
    query: id
  })
}
export function updateApplicability(data) {
  return request({
    url: '/adminip/adjuts_detect_switch/',
    method: 'post',
    data: data
  })
}
export function updateQos(data) {
  return request({
    url: '/adminip/adjuts_detect_switch/',
    method: 'post',
    data: data
  })
}
