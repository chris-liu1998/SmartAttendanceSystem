import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';
import SERVICE_PATH from "./configs";
import NProgress from 'nprogress' // 引入nprogress插件
import 'nprogress/nprogress.css'  // 这个nprogress样式必须引入

import HighchartsVue from 'highcharts-vue'

Vue.use(HighchartsVue)
//配置 axios
import axios from 'axios'
import VueAxios from 'vue-axios'
Vue.use(VueAxios, axios);

//配置 vue-json-excel
import JsonExcel from 'vue-json-excel'
Vue.component('downloadExcel', JsonExcel)

//配置 vue-xlsx-table
import vueXlsxTable from 'vue-xlsx-table'
Vue.use(vueXlsxTable, { rABS: false })

/**
 * 安装依赖包，在src目录下创建ecxel文件夹，放置相应文件
 * npm install -S file-saver xlsx
 * npm install -D script-loader
 */

Vue.config.productionTip = false
Vue.prototype.SERVICE_PATH = SERVICE_PATH;

NProgress.configure({showSpinner: false});
axios.interceptors.request.use(
  config => {
    NProgress.start() // 设置加载进度条(开始..)
    return config
  },
  error => {
    return Promise.reject(error)
  }
)
// axios响应拦截器
axios.interceptors.response.use(
  function (response) {
    NProgress.done() // 设置加载进度条(结束..)
    return response
  },
  function (error) {
    return Promise.reject(error)
  }
)


// axios.defaults.withCredentials=true
//登录拦截器
router.beforeEach((to, from, next) => {
  NProgress.start()
  if (to.meta.requireAuth) {
    if (store.state.userid) {
      next()
    } else {
      next({
        path: 'login',
        query: { redirect: to.fullPath }
      })
    }
  } else {
    next()
  }
})
router.afterEach(() => {
  NProgress.done()
})
new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')

