import request from '@/utils/polaris_request'

export function fetchList(page) {
  return request({
    url: '/nameidpolicy/universal_matching_nameidpolicy/',
    method: 'get',
    params: page
  })
}
export function create(data) {
  return request({
    url: '/nameidpolicy/',
    method: 'post',
    data: data
  })
}
export function update(data, id) {
  return request({
    url: '/nameidpolicy/' + id + '/',
    method: 'put',
    data: data,
    query: id
  })
}
export function deleteid(id) {
  return request({
    url: '/nameidpolicy/' + id + '/',
    method: 'delete',
    query: id
  })
}
