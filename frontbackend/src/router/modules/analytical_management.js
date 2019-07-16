import Layout from '@/layout'

const platformRouter = {
  path: '/analytical_management',
  component: Layout,
  redirect: '/analytical_management/analytical_management',
  name: 'Table',
  meta: {
    title: '解析管理',
    icon: 'table'
  },
  children: [
    {
      path: 'analytical',
      component: () => import('@/views/analytical_management/analytical'),
      name: 'analytical',
      meta: { title: '解析配置' }
    },
    {
      path: 'policy',
      component: () => import('@/views/analytical_management/nameidpolicy'),
      name: 'policy',
      meta: { title: '策略管理' }
    },
    {
      path: 'multiple',
      component: () => import('@/views/analytical_management/multiple'),
      name: 'multiple',
      meta: { title: '批量工具' }
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
