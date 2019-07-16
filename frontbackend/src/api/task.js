import request from '@/utils/polaris_request'

export function fetchList(page) {
  return request({
    url: '/detecttask/universal_matching_taskname/',
    method: 'get',
    params: page
  })
}
export function create(data) {
  return request({
    url: '/detecttask/',
    method: 'post',
    data: data
  })
}
export function update(data, id) {
  return request({
    url: '/detecttask/' + id + '/',
    method: 'put',
    data: data,
    query: id
  })
}
export function deleteid(id) {
  return request({
    url: '/detecttask/' + id + '/',
    method: 'delete',
    query: id
  })
}
