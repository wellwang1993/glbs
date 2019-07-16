import request from '@/utils/polaris_request'

export function fetchList(page) {
  return request({
    url: '/cname/get_third_resource_info/',
    method: 'get',
    params: page
  })
}
export function create(data) {
  return request({
    url: '/cname/',
    method: 'post',
    data: data
  })
}

export function update(data, id) {
  return request({
    url: '/cname/' + id + '/',
    method: 'put',
    data: data,
    query: id
  })
}

export function deleteid(id) {
  return request({
    url: '/cname/' + id + '/',
    method: 'delete',
    query: id
  })
}
