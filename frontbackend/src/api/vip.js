import request from '@/utils/polaris_request'

export function vipApplicability(page) {
  return request({
    url: '/vipdevice/adjust_resource/',
    method: 'post',
    data: page
  })
}
export function vipUpdown(page) {
  return request({
    url: '/vipdevice/maintain_resource/',
    method: 'post',
    data: page
  })
}
export function fetchList(page) {
  return request({
    url: '/vipdevice/get_all_resource_info/',
    method: 'get',
    params: page
  })
}
export function create(data) {
  return request({
    url: '/vipdevice/',
    method: 'post',
    data: data
  })
}

export function update(data, id) {
  return request({
    url: '/vipdevice/' + id + '/',
    method: 'put',
    data: data,
    query: id
  })
}

export function deleteid(id) {
  return request({
    url: '/vipdevice/' + id + '/',
    method: 'delete',
    query: id
  })
}
