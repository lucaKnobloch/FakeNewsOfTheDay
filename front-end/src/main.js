// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Example from './example/Example.vue'
Vue.config.productionTip = true
/* eslint-disable no-new */
new Vue({
  render: h => h(Example)
}).$mount('#app')