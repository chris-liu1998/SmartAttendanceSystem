<template>
  <nav>
    <v-app-bar flat app>
      <v-app-bar-nav-icon elevation="3" @click.stop="setDrawer"></v-app-bar-nav-icon>
      <v-toolbar-title class="hidden-sm-and-down font-weight-light" v-text="$route.name" />
      <v-spacer></v-spacer>

      <v-avatar>
        <img :src="imgurl" alt="头像" />
      </v-avatar>

      <v-menu bottom left offset-y origin="top right" transition="scale-transition">
        <template v-slot:activator="{ attrs, on }">
          <v-btn
            class="ml-2"
            min-width="0"
            text
            v-bind="attrs"
            v-on="on"
          >{{username==""? "管理员": username}}</v-btn>
        </template>
        <v-list>
          <v-list-item to="/userprofile">
            <v-list-item-icon>
              <v-icon>mdi-account</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>个人中心</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-divider />
          <!-- <v-list-item to="/login">
            <v-list-item-icon>
              <v-icon>mdi-exit-to-app</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>退出登录</v-list-item-title>
            </v-list-item-content>
          </v-list-item>-->
          <v-list-item @click="exit">
            <v-list-item-icon>
              <v-icon>mdi-exit-to-app</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>退出登录</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-navigation-drawer
      mobile-breakpoint="800"
      v-model="drawer"
      app
      :color="color"
      :mini-variant.sync="miniVariant"
      mini-variant-width="62"
      :src="bg"
      dark
    >
      <v-list nav class="py-0">
        <v-list-item two-line :class="miniVariant && 'px-0'">
          <v-list-item-avatar class="align-self-center" color="white" contain>
            <v-img src="../assets/logo.png" max-height="30" />
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title>智慧考勤系统</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>
        <div v-for="link in links" :key="link.title" class="my-2">
          <v-list-item v-if="!link.subs" link :to="link.path" active-class="border">
            <v-list-item-icon class="active">
              <v-icon>{{ link.icon }}</v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title class="font-weight-bold">{{ link.title }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-group v-else :key="link.title" active-class="blue lighten-2 white--text">
            <template v-slot:activator :value="false" link :to="link.path">
              <v-list-item-icon>
                <v-icon>{{ link.icon }}</v-icon>
              </v-list-item-icon>

              <v-list-item-content>
                <v-list-item-title class="font-weight-bold">{{ link.title }}</v-list-item-title>
              </v-list-item-content>
            </template>
            <v-list-item
              v-for="sub in link.subs"
              :to="sub.path"
              :key="sub.title"
              link
              active-class="border white--text"
            >
              <v-list-item-icon class="active">
                <v-icon>{{ sub.icon }}</v-icon>
              </v-list-item-icon>
              <v-list-item-title class="font-weight-bold">{{ sub.title }}</v-list-item-title>
            </v-list-item>
          </v-list-group>
        </div>
      </v-list>
    </v-navigation-drawer>
  </nav>
</template>



<script>
export default {
  name: "Navbar",

  data() {
    return {
      imgurl: null,
      drawer: true,
      links: [],
      flag: {},
      all_links: [
        {
          title: "主页",
          icon: "fas fa-tachometer-alt",
          path: "/",
          flag: ["0", "1", "2"]
        },
        {
          title: "考勤管理",
          icon: "fas fa-tasks",
          path: "/attendance",
          flag: ["1", "2"],
          subs: [
            {
              title: "打卡",
              icon: "fas fa-camera-retro",
              path: "/attendance/facerecord",
              flag: ["1", "2"]
            },
            {
              title: "考勤记录",
              icon: "fas fa-clipboard",
              path: "/attendance/record",
              flag: ["1", "2"]
            }
          ]
        },
        {
          title: "请假",
          icon: "fas fa-sign-out-alt",
          path: "/leave",
          flag: ["0", "1", "2"],
          subs: [
            {
              title: "请假申请",
              icon: "fas fa-envelope-open-text",
              path: "/leave/newLeave",
              flag: ["1", "2"]
            },
            {
              title: "请假记录",
              icon: "mdi-image",
              path: "/leave/LeaveList_e",
              flag: ["1", "2"]
            },
            {
              title: "草稿箱",
              icon: "fas fa-edit",
              path: "/leave/LeaveDraft",
              flag: ["1", "2"]
            },
            {
              title: "请假处理",
              icon: "fas fa-calendar-minus",
              path: "/leave/LeaveList_m",
              flag: ["0", "1"]
            }
          ]
        },
        {
          title: "统计数据",
          icon: "fas fa-chart-line",
          path: "/statistics",
          flag: ["0", "1"],
          subs: [
            {
              title: "考勤排行",
              icon: "fas fa-list-ol",
              path: "/statistics/rank",
              flag: ["0", "1"]
            }
          ]
        },
        {
          title: "公司管理",
          icon: "fas fa-users-cog",
          path: "/administrator",
          flag: ["0"],
          subs: [
            {
              title: "账户管理",
              icon: "fas fa-users",
              path: "/administrator/account",
              flag: ["0"]
            },
            {
              title: "员工管理",
              icon: "fas fa-id-card",
              path: "/administrator/employee",
              flag: ["0"]
            },
            {
              title: "考勤设置",
              icon: "mdi-image",
              path: "/administrator/attendancesetting",
              flag: ["0"]
            }
          ]
        },
        // {
        //   title: "个人中心",
        //   icon: "mdi-help-box",
        //   path: "/userprofile",
        //   flag: ["1", "2"]
        // }
      ],
      color: "primary",
      // colors: ["primary", "blue", "success", "red", "teal"],

      miniVariant: false,
      background: false,
      isMini: true,
      // 未读消息
      UnreadMesssage: {},
      // 员工姓名
      username: ""
    };
  },
  computed: {
    bg() {
      return this.background
        ? "https://cdn.vuetifyjs.com/images/backgrounds/bg-2.jpg"
        : undefined;
    }
  },
  mounted() {
    this.flag = localStorage.getItem("flag");
    // this.flag = 2;
    this.link_filter();
    //axios获取账户信息
    var accountoneurl = this.SERVICE_PATH + "account/one";
    var accountFormData = new FormData();
    accountFormData.append("account", localStorage.getItem("userid"));
    this.axios
      .post(accountoneurl, accountFormData, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        }
      })
      .then(res => {
        // console.log(res.data.data)
        if (res.data.code == 200) {
          if (res.data.data.avatar == null || res.data.data.avatar == "") {
            this.imgurl =
              "https://demos.creative-tim.com/vue-material-dashboard/img/marc.aba54d65.jpg";
          } else {
            this.imgurl =
              "http://8.129.163.104/images/avatar/" + res.data.data.avatar;
          }
        }
      })
      .catch(err => {
        console.log(err);
      });
    // axios 获取 message.json
    // this.axios
    //   .get("./message.json")
    //   .then((res) => {
    //     //console.log(res.data)
    //     this.UnreadMesssage = res.data;
    //   })
    //   .catch((err) => {
    //     console.log(err);
    //   });

    //axios获取个人信息
    if (localStorage.getItem("userid") != "Admin") {
      let employeeoneurl = this.SERVICE_PATH + "employee/one";
      let eidFormData = new FormData();
      eidFormData.append("employee_id", localStorage.getItem("userid"));
      this.axios
        .post(employeeoneurl, eidFormData, {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded"
          }
        })
        .then(res => {
          // console.log(res.data)
          if (res.data.code == 200) {
            this.username = res.data.data.employee_name;
            this.$store.commit("getName", this.username);
          }
          // else{
          //   this.username = "Admin"
          //   console.log(this.username)
          // }
        })
        .catch(err => {
          console.log(err);
        });
    }
  },
  methods: {
    link_filter() {
      for (var i = 0; i < this.all_links.length; i++) {
        var link = this.all_links[i];
        // console.log(link.flag);
        var temp = {};
        var sub = [];
        var hasValue = false;
        for (var j = 0; j < link.flag.length; j++) {
          if (link.flag[j] == this.flag.toString()) {
            hasValue = true;
            temp.title = link.title;
            temp.icon = link.icon;
            temp.path = link.path;
            if ("subs" in link) {
              for (var t = 0; t < link.subs.length; t++) {
                var sub_temp = {};
                var sub_hasValue = false;
                for (var d = 0; d < link.subs[t].flag.length; d++) {
                  if (this.flag == link.subs[t].flag[d].toString()) {
                    sub_hasValue = true;
                    sub_temp.title = link.subs[t].title;
                    sub_temp.icon = link.subs[t].icon;
                    sub_temp.path = link.subs[t].path;
                  }
                }
                if (sub_hasValue) {
                  sub.push(sub_temp);
                }
              }
              if (sub.length > 0) {
                temp.subs = sub;
              }
            }
          }
        }
        if (hasValue) {
          this.links.push(temp);
        }
      }
    },
    setDrawer() {
      if (this.$vuetify.breakpoint.lgAndUp) {
        this.miniVariant = !this.miniVariant;
      } else {
        this.drawer = !this.drawer;
      }
    },
    //退出
    exit() {
      this.$store.commit("LOGOUT");
      this.$router.push({ path: "/login" });
    }
    // messageClick() {
    //   this.$router.push("leave/LeaveList_e");
    //   //消息点击事件
    // },
  }
};
</script>
<style scoped>
.border {
  border-left: 4px solid #f5b834;
}
.active {
  color: #399cff !important;
}
</style>