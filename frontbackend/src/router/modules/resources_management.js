import Layout from '@/layout'

const platformRouter = {
  path: '/resources_management',
  component: Layout,
  redirect: '/resources_management/resources_management',
  name: 'Table',
  meta: {
    title: '资源管理',
    icon: 'table'
  },
  children: [
    {
      path: 'vip',
      component: () => import('@/views/resolution_group/vip'),
      name: 'vip',
      meta: { title: 'vip管理' }
    },
    {
      path: 'cname',
      component: () => import('@/views/resolution_group/cname'),
      name: 'cname',
      meta: { title: 'cname管理' }
    },
    {
      path: 'multiple',
      component: () => import('@/views/resolution_group/multiple'),
      name: 'multiple',
      meta: { title: '批量操作' }
    }
  ]
  /*
    {
      path: 'drag-table',
      component: () => import('@/views/table/drag-table'),
      name: 'DragTable',
      meta: { title: 'Drag Table' }
    },
    {
      path: 'inline-edit-table',
      component: () => import('@/views/table/inline-edit-table'),
      name: 'InlineEditTable',
      meta: { title: 'Inline Edit' }
    },
    {
      path: 'complex-table',
      component: () => import('@/views/table/complex-table'),
      name: 'ComplexTable',
      meta: { title: 'Complex Table' }
    }
  ]
  */
}
export default platformRouter
