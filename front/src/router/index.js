import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [{
  path: '/login',
  name: '登录',
  component: () => import('@/views/login/Login')
},
{
  path: '/',
  component: () => import('@/commons/Layout'),
  children: [
    // 首页
    {
      name: '主页',
      path: '',
      component: () => import('@/views/Index'),
      meta: {
        requireAuth: true
      }
    },
    {
      name: '管理员/账号管理',
      path: 'administrator/account',
      component: () => import('@/views/administrator/CreateAccount'),
      meta: {
        requireAuth: true
      }
    },
    {
      name: '管理员/员工管理',
      path: 'administrator/employee',
      component: () => import('@/views/administrator/HandleE'),
      meta: {
        requireAuth: true
      }
    },
    {
      name: '管理员/考勤设置',
      path: 'administrator/attendancesetting',
      component: () => import('@/views/administrator/AttendanceSetting'),
      meta: {
        requireAuth: true
      }
    },
    // 请假列表
    {
      path: 'leave/LeaveList_e',
      name: '请假/请假记录',
      component: () => import('@/views/leave/LeaveList_e'),
      meta: {
        requireAuth: true
      }
    },
    // 请假申请
    {
      path: 'leave/newLeave',
      name: '请假/请假申请',
      component: () => import('@/views/leave/LeaveNew'),
      meta: {
        requireAuth: true
      }
    },
    // 请假草稿箱
    {
      path: 'leave/LeaveDraft',
      name: '请假/草稿箱',
      component: () => import('@/views/leave/LeaveDraft'),
      meta: {
        requireAuth: true
      }
    },
    // 请假处理
    {
      path: 'leave/LeaveList_m',
      name: '请假/请假处理',
      component: () => import('@/views/leave/LeaveList_m'),
      meta: {
        requireAuth: true
      }
    },
    //考勤排行
    {
      path: 'statistics/rank',
      name: '统计数据/考勤排行',
      component: () => import('@/views/statistics/Rank'),
      meta: {
        requireAuth: true
      }
    },
    //考勤
    {
      path: 'attendance/record',
      name: '考勤管理/考勤记录',
      component: () => import('@/views/attendance/AttendanceRecord'),
      meta: {
        requireAuth: true
      }
    },
    //人脸打卡
    {
      path: 'attendance/facerecord',
      name: '考勤管理/打卡',
      component: () => import('@/views/attendance/FaceRecord'),
      meta: {
        requireAuth: true
      }
    },

    //个人中心
    {
      path: 'userprofile',
      name: '个人中心',
      component: () => import('@/views/user/UserInfo')
    }
  ]
}
]

const router = new VueRouter({
  routes
})

export default router
