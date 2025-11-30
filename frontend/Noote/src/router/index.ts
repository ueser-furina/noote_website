import { createRouter, createWebHistory } from 'vue-router'
import { authService } from '../services/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/Home.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/Register.vue'),
    },
    {
      path: '/notes',
      name: 'notes',
      component: () => import('../views/NoteList.vue'),
    },
    {
      path: '/notes/:id',
      name: 'note-detail',
      component: () => import('../views/NoteDetail.vue'),
    },
    {
      path: '/my-notes',
      name: 'my-notes',
      component: () => import('../views/MyNotes.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/create-note',
      name: 'create-note',
      component: () => import('../views/CreateNote.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/collections/public',
      name: 'public-collections',
      component: () => import('../views/PublicCollections.vue'),
    },
    {
      path: '/my-collections',
      name: 'my-collections',
      component: () => import('../views/MyCollections.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/collections/:id',
      name: 'collection-detail',
      component: () => import('../views/CollectionDetail.vue'),
    },
  ],
})

// 路由守衛
router.beforeEach((to, _from, next) => {
  if (to.meta.requiresAuth && !authService.isAuthenticated()) {
    next('/login')
  } else {
    next()
  }
})

export default router
