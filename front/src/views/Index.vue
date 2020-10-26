<!--主页模板-->
<template>
  <v-container class="fill-height pb-0 px-0">
    <v-row no-gutters>
      <v-col cols="auto" md="6" align-self="start">
        <v-row>
          <v-col>
            <greeting-card class="mt-auto"></greeting-card>
          </v-col>
        </v-row>
      </v-col>
      <!-- <v-divider vertical></v-divider> -->
      <v-col md="6">
        <v-row class="pa-0" no-gutters>
          <v-col cols="auto">
            <weather-card></weather-card>
          </v-col>
          <v-col>
            <history></history>
          </v-col>
        </v-row>
        <v-row>
          <v-col></v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col class="pb-n7" cols="auto" md="4">
        <todo-list :hidden="button_hidden"></todo-list>
      </v-col>
      <v-col class="pb-n7" md="5">
        <stats-chart></stats-chart>
      </v-col>
      <v-col>
        <simple-rank></simple-rank>
      </v-col>
    </v-row>
  </v-container>
</template>




<script>
import GreetingCard from "@/components/index/GreetingCard";
import TodoList from "@/components/index/TodoList";
import WeatherCard from "@/components/index/WeatherCard";
import History from "@/components/index/History";
import StatsChart from "@/components/index/StatsChart";
// import Record from "@/components/Index/record.vue";
import SimpleRank from "@/components/index/SimpleRank";
// import Features from "../components/Index/features.vue";
import { mapState } from "vuex";
export default {
  name: "Index",
  data() {
    return {
      user_id: {},
      powers: ["管理员", "部门经理", "员工"],
      dialog: false,
     
      button_hidden: true,
    };
  },
  computed: {
    ...mapState({ flag: "flag" }),
  },
  components: {
    "greeting-card": GreetingCard,
    "todo-list": TodoList,
    "weather-card": WeatherCard,
    history: History,
    "stats-chart": StatsChart,
    "simple-rank": SimpleRank,
    // RightBar,
    // Features,
  },
  methods: {
    checkFaceInfo() {
      //通过flag和是否拥有face信息，通知用户前往打卡
      if (this.flag != 0) {
        this.axios
          .get(this.SERVICE_PATH + "facechecked", {
            params: {
              user_id: this.user_id,
            },
          })
          .then((res) => {
            if (res.data.data == false) {
              this.faceAcquisition();
            }
          });
      }
    },
    faceAcquisition() {
      this.dialog = true;
    },
    show() {
      //根据flag对当前页面进行功能显示/隐藏
      if (this.flag == "0") {
        //管理员
        document.getElementById("employee_fea").style.display = "none";
        document.getElementById("employee_rec").style.display = "none";
        document.getElementById("admin_fea").style.display = "inline";
      } else {
        //员工和部门经理
        document.getElementById("admin_fea").style.display = "none";
        document.getElementById("employee_fea").style.display = "inline";
        document.getElementById("employee_rec").style.display = "inline";
      }
    },
    face_record() {
      this.dialog = false;
      this.$router.push({
        path: "attendance/facerecord",
      });
    },
  },

  mounted() {
    this.user_id = localStorage.getItem("userid");
    this.button_hidden = false;
    // this.show();
    this.checkFaceInfo();
  },
};
</script>

<style>
#Title {
  float: left;
  margin-left: 5%;
}

.feature {
  float: right;
  width: 45%;
  margin-right: 5%;
  background-color: rgb(47, 241, 255);
}

.SparkLine {
  float: left;
  width: 45%;
  margin-left: 10%;
  background-color: rgb(47, 241, 255);
}

.rank {
  float: right;
  width: 30%;
  margin-right: 5%;
}

#rightbar {
  margin-top: 10%;
}
</style>