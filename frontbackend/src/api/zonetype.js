import request from '@/utils/polaris_request'

export function fetchList(page) {
  return request({
    url: '/zonetype/universal_matching_zonetype/',
    method: 'get',
    params: page
  })
}
export function fetchOne(id) {
  return request({
    url: '/zonetype/universal_matching_zonetype/',
    method: 'get',
    params: { id }
  })
}
export function create(data) {
  return request({
    url: '/zonetype/',
    method: 'post',
    data: data
  })
}

export function update(data, id) {
  return request({
    url: '/zonetype/' + id + '/',
    method: 'put',
    data: data,
    query: id
  })
}

export function deleteid(id) {
  return request({
    url: '/zonetype/' + id + '/',
    method: 'delete',
    query: id
  })
}
