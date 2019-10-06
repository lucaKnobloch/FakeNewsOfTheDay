import Vue from 'vue'
import Router from 'vue-router'
import Example from '../example/Example.vue'
import PurposePage from '@/components/PurposePage'
import About from '../components/About'
import Contact from '@/components/Contact'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Net',
      component: Example
    },
    {
      path: '/purposepage',
      name: 'PurposePage',
      component: PurposePage
    },
    {
      path: '/about',
      name: 'About',
      component: About
    },
    {
      path: '/contact',
      name: 'Contact',
      component: Contact
    }
  ]
})
