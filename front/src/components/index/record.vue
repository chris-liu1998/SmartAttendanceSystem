<template>
    <v-container>
        <div id="myChart" ref="myChart" style="width:500px;height:400px">
    </div>

    </v-container>

</template>

<script>
let echarts = require('echarts/lib/echarts')
require('echarts/lib/chart/line')
require('echarts/lib/component/tooltip')
require('echarts/lib/component/title')
export default {
  name: 'record',
  data(){
    return{
      days:[],
      hours:[],
      user_id:{},
    }
  },
  methods:{
    drawLine(){
      let myChart = echarts.init(this.$refs.myChart)

      myChart.setOption({
        title:{text:'一周打卡统计'},
        tooltip:{},
        xAxis:{
          data:this.days
        },
        yAxis:{

        },
        series:{
          name:'工作时长',
          type: 'line',
          data: this.hours
        }

      })
    },
    getDays(){
      let today = new Date()
      var one_day = 1000*60*60*24

      //将时间设定在7天前
      today.setTime(today.getTime()-7*one_day)

      for(var i = 0;i<7;i++){
        var tDay = today.getDate() //获取日
        var tMonth = today.getMonth()+1 //获取月份
        //将日期存入数组
        this.days.push(tMonth+"-"+tDay)
        //时间跳转到下一天
        var target_day = today.getTime()+one_day
        today.setTime(target_day)
      }
    },
    getHours(){
      this.axios
        .get(
          this.SERVICE_PATH +
            "selfrecord",{
              params:{
                user_id: this.user_id
              }
            }
        )
        .then(res => {
          this.hours = res.data.data;
        });
      this.getDays()
      this.drawLine()
    }
  },
  mounted(){
    this.user_id =localStorage.getItem('userid')
    this.getHours()


  }
}
</script>


<style>

</style>