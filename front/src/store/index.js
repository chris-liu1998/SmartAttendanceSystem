import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

//登录拦截器
export default new Vuex.Store({
  state: {
    userid: window.localStorage.getItem('userid') == null ? '' : window.localStorage.getItem('userid'),
    flag: window.localStorage.getItem('flag') == null ? '' : window.localStorage.getItem('flag'),
    departmentid: window.localStorage.getItem('departmentid') == null ? '' : window.localStorage.getItem('departmentid'),
    name: "",
    record_id: null,
    last_time:null,
  },
  mutations: {
    login(state, login) {
      const { userid, flag, departmentid } = login
      state.userid = userid
      state.flag = flag
      state.departmentid = departmentid
      window.localStorage.setItem('userid', userid)
      window.localStorage.setItem('flag', flag)
      window.localStorage.setItem('departmentid', departmentid)
      console.log(state.flag);
    },
    LOGOUT(state) {
      localStorage.clear();
      state.userid = null;
      state.flag = null;
      state.departmentid = null;
    },
    getName(state, name) {
      state.name = name;
    },
    getRecord(state, record_id) {
      state.record_id = record_id;
    },
    getLast(state, lasttime) {
      state.last_time = lasttime;
    }
  },
  actions: {
  },
  modules: {
  }
})


