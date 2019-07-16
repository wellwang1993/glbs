import request from '@/utils/polaris_request'

export function fetchList(page) {
  return request({
    url: '/dnstype/universal_matching_dnstype/',
    method: 'get',
    params: page
  })
}
export function create(data) {
  return request({
    url: '/dnstype/',
    method: 'post',
    data: data
  })
}

export function update(data, id) {
  return request({
    url: '/dnstype/' + id + '/',
    method: 'put',
    data: data,
    query: id
  })
}

export function deleteid(id) {
  return request({
    url: '/dnstype/' + id + '/',
    method: 'delete',
    query: id
  })
}
