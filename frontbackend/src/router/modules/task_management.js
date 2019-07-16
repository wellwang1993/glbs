import Layout from '@/layout'

const platformRouter = {
  path: '/task_management',
  component: Layout,
  redirect: '/task_management/task_management',
  name: 'Table',
  meta: {
    title: '任务管理',
    icon: 'table'
  },
  children: [
    {
      path: 'probe',
      component: () => import('@/views/task_management/probe'),
      name: 'dnstype',
      meta: { title: '探针管理' }
    },
    {
      path: 'standard',
      component: () => import('@/views/task_management/standard'),
      name: 'Dnsip',
      meta: { title: '有效性设置' }
    },
    {
      path: 'task',
      component: () => import('@/views/task_management/task'),
      name: 'DragTable',
      meta: { title: '任务管理' }
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
