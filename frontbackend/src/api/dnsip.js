import request from '@/utils/polaris_request'

export function fetchDnstype(page) {
  return request({
    url: '/dnstype/',
    method: 'get'
  })
}
export function fetchList(page) {
  return request({
    url: '/dnsip/universal_matching_dnsip/',
    method: 'get',
    params: page
  })
}
export function create(data) {
  return request({
    url: '/dnsip/',
    method: 'post',
    data: data
  })
}

export function update(data, id) {
  return request({
    url: '/dnsip/' + id + '/',
    method: 'put',
    data: data,
    query: id
  })
}

export function deleteid(id) {
  return request({
    url: '/dnsip/' + id + '/',
    method: 'delete',
    query: id
  })
}
