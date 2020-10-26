<template>
  <v-card class="ma-3 mb-auto">
    <v-list-item>
      <v-list-item-avatar tile size="100" rounded class="mt-n8">
        <v-sheet color="yellow lighten-2" width="70" height="70" elevation="5" rounded>
          <v-icon dark large>fas fa-chart-area</v-icon>
        </v-sheet>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-title class="text-h6 font-weight-black grey--text text--darken-3">近七日内工作时长</v-list-item-title>
      </v-list-item-content>
    </v-list-item>

    <v-card-text>
      <div id="myChart" ref="myChart" style="width:100%;height:265px"></div>
    </v-card-text>
  </v-card>
</template>

<script>
let echarts = require("echarts/lib/echarts");
require("echarts/lib/chart/line");
require("echarts/lib/component/tooltip");
require("echarts/lib/component/title");
export default {
  name: "StatsChart",
  data() {
    return {
      days: [],
      hours: [],
      user_id: ""
    };
  },
  methods: {
    myCallback() {
      console.log("this is callback function");
    },
    //绘制图像
    drawLine() {
      let myChart = echarts.init(this.$refs.myChart);

      myChart.setOption({
        grid: {
          top: "10",
          x: 50,

          y: 50,
          x2: 70,
          y2: 60
        },
        tooltip: {},
        xAxis: {
          data: this.days
        },
        yAxis: {
          type: "value"
        },
        series: {
          name: "工作时长",
          type: "line",
          data: this.hours,
          areaStyle: {},
          itemStyle : {  
                                normal : {  
                                    lineStyle:{  
                                        color:'#399cff'  
                                    }  ,
                                    areaStyle:{
                                        color:'#6796eb'
                                    }
                                }  
                            },  
        }
      });
    },
    // 得到当前时间及其前7天
    getDays() {
      let today = new Date();
      var one_day = 1000 * 60 * 60 * 24;

      //将时间设定在7天前
      today.setTime(today.getTime() - 7 * one_day);

      for (var i = 0; i < 7; i++) {
        var tDay = today.getDate(); //获取日
        var tMonth = today.getMonth() + 1; //获取月份
        //将日期存入数组
        this.days.push(tMonth + "-" + tDay);
        //时间跳转到下一天
        var target_day = today.getTime() + one_day;
        today.setTime(target_day);
      }
    },
    async getHours() {
      await this.axios
        .get(this.SERVICE_PATH + "simplerecord", {
          params: {
            user_id: this.user_id
          }
        })
        .then(res => {
          this.hours = res.data.data;
          console.log(this.hours);
        });
      this.getDays();
      this.drawLine();
    }
  },
  mounted() {
    this.user_id = localStorage.getItem("userid");
    this.getHours();
  }
};
</script>

<style scoped>
</style>