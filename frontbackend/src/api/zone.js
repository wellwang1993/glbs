import request from '@/utils/polaris_request'

export function generateConfig(page) {
  return request({
    url: '/dnszone/push_zone/',
    method: 'get',
    params: page
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
    url: '/dnszone/universal_matching_dnszone/',
    method: 'get',
    params: page
  })
}
export function create(data) {
  return request({
    url: '/dnszone/',
    method: 'post',
    data: data
  })
}

export function update(data, id) {
  return request({
    url: '/dnszone/' + id + '/',
    method: 'put',
    data: data,
    query: id
  })
}

export function deleteid(id) {
  return request({
    url: '/dnszone/' + id + '/',
    method: 'delete',
    query: id
  })
}
