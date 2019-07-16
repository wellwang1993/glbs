import request from '@/utils/polaris_request'

export function fetchList(page) {
  return request({
    url: '/deviceavailabilitystandard/universal_matching_standard/',
    method: 'get',
    params: page
  })
}
export function create(data) {
  return request({
    url: '/deviceavailabilitystandard/',
    method: 'post',
    data: data
  })
}
export function update(data, id) {
  return request({
    url: '/deviceavailabilitystandard/' + id + '/',
    method: 'put',
    data: data,
    query: id
  })
}
export function deleteid(id) {
  return request({
    url: '/deviceavailabilitystandard/' + id + '/',
    method: 'delete',
    query: id
  })
}
