import Layout from '@/layout'

const platformRouter = {
  path: '/platform_management',
  component: Layout,
  redirect: '/platform_management/platform_management',
  name: 'Table',
  meta: {
    title: '平台管理',
    icon: 'table'
  },
  children: [
    {
      path: 'dnstype',
      component: () => import('@/views/platform_management/dnstype'),
      name: 'dnstype',
      meta: { title: '解析组管理' }
    },
    {
      path: 'dnsip',
      component: () => import('@/views/platform_management/dnsip'),
      name: 'Dnsip',
      meta: { title: '权威dns管理' }
    },
    {
      path: 'zonetype',
      component: () => import('@/views/platform_management/zonetype'),
      name: 'DragTable',
      meta: { title: 'zone类型管理' }
    },
    {
      path: 'zone',
      component: () => import('@/views/platform_management/zone'),
      name: 'Zone',
      meta: { title: 'zone管理' }
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
