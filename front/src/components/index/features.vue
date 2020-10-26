<template>
  <div>
    <v-container>
      <v-row v-for="fg in fgNum" :key="fg">
        <v-col v-for="n in features.slice((fg-1)*3,fg*3)" :key="n.name" align="center" cols="12" md="4">
          <v-card @click="jump($event,n.path)">
            <!--                        <v-row>
                        <v-col>
                        <v-img
                        src="https://picsum.photos/350/165?random"
                        class="grey lighten-2"
                        min-width="180"
                        min-height="120"
                        >
                        </v-img>                            
                        </v-col>
                     </v-row>

                        <v-row>
                            <v-divider>
                            </v-divider>
                        </v-row>
            -->
            <v-row>
              <v-col align="center">
                <div id="div" min-width="100" height="40">{{n.name}}</div>
              </v-col>
            </v-row>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>



<script>
export default {
  data: () => ({
    user_id: {},
    flag: {},
    allFeatures: [
      { name: "打卡", requrirement: ["1", "2"], path: "attendance/facerecord" },
      { name: "请假申请", requrirement: ["1", "2"], path: "leave/newLeave" },
      { name: "请假进度查看", requrirement: ["1", "2"], path: "leave/LeaveList_e" },
      { name: "请假管理", requrirement: ["0", "1"], path: "leave/LeaveList_m" },
      { name: "修改个人信息", requrirement: ["0", "1", "2"], path: "" },
      { name: "新增员工", requrirement: ["0"], path: "administrator/account" },
      { name: "管理员工", requrirement: ["0"], path: "administrator/employee" },
    ],
    features: [],
    fgNum: 0,
  }),
  methods: {
    jump(event, value) {
      console.log(event);
      this.$router.push(value);
    },
  },
  mounted() {
    this.user_id = localStorage.getItem("userid");
    this.flag = localStorage.getItem("flag");
    for (var i = 0; i < this.allFeatures.length; i++) {
      var requrirement = this.allFeatures[i].requrirement;
      for (var j = 0; j < requrirement.length; j++) {
        if (requrirement[j] == this.flag) {
          this.features.push(this.allFeatures[i]);
          break;
        }
      }
    }
    this.fgNum = parseInt((this.features.length + 2) / 3);
    console.log(this.fgNum);

    //console.log(this.features)//获得所有当前用户所能使用的功能
  },
};
</script>

<style>
#div {
  width: 100;
}
</style>