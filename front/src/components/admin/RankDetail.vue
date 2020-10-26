<template>
<v-container>
  <div
  class="calendar"
  >
  <v-card>
    <v-sheet
      tile
      height="60"
      color="grey lighten-3"
      class="d-flex"
    >
      <v-btn
        icon
        class="ma-2"
        @click="$refs.calendar.prev()"
      >
        <v-icon>mdi-chevron-left</v-icon>
      </v-btn>

      <v-select
        v-model="type"
        :items="types"
        dense
        outlined
        hide-details
        class="ma-2"
        label="显示方式"
      ></v-select>

      <div style="width:200px; text-align:center;line-height:60px" ><h2>{{value}}</h2></div>

      <v-select
        v-model="weekday"
        :items="weekdays"
        dense
        outlined
        hide-details
        label="显示内容"
        class="ma-2"
      ></v-select>

      <v-spacer></v-spacer>

      <v-btn
        icon
        class="ma-2"
        @click="$refs.calendar.next()"
      >
        <v-icon>mdi-chevron-right</v-icon>
      </v-btn>
    </v-sheet>


    <v-sheet height="600">
      <v-calendar
        v-if="reload"
        ref="calendar"
        v-model="value"
        :weekdays="weekday"
        :type="type"
        :events="events"
        :event-overlap-mode="mode"
        :event-overlap-threshold="30"
        :event-color="getEventColor"
        @change="setEvents"
      ></v-calendar>
    </v-sheet>
  </v-card>
  </div>
  </v-container>
</template>


<script>

  export default {
      inject:['reload'],
    props:["employee",],
    data: () => ({
        user_id:"",
        reload:true,
        mode: 'stack',
        type: 'month',
        types: [
        {text:"按月显示",value:'month'},
        {text:"按周显示",value: 'week'},
        ],
      weekday: [0, 1, 2, 3, 4, 5, 6],
      weekdays: [
        { text: '周日 - 周六', value: [0, 1, 2, 3, 4, 5, 6] },
        { text: '周一 - 周六', value: [1, 2, 3, 4, 5, 6] },
      ],
      value: '',
      events: [],
      colors: ['blue', 'green', 'orange', 'red'],
      names: ['出勤', '请假', '迟到早退', '缺勤'],
      eventTemp:[]
    }),
    methods: {
      //向后台请求记录
      // async 和await 联合使用实现同步axios
      async getEvents ({ start, end }) {

        //start 是日历上显示的第一天，end是日历上显示的最后一天
        //数据库中的between是左闭右开
        var start_day = start.date
        var end_day = end.date

        // alert(this.user_id+": "+start_day+" "+end_day)
          this.eventTemp=[]
          await this.axios
          .get(this.SERVICE_PATH + "selfrecord", {
            params: {
              user_id: this.user_id,
              start_day: start_day,
              end_day: end_day 
            },
          })
          .then((res) => {
            this.eventTemp= res.data.data
            //alert("获取成功")
          });
      },

      // 向日历中添加记录
      async setEvents({ start, end }){
        await this.getEvents ({ start, end }) //请求考勤记录
        
        this.events=[]  //清空已有记录，重新获取
        
        //alert(this.eventTemp.length)
        //alert(this.eventTemp[0].name)
        //alert(this.getColor(this.eventTemp[0].name))
        for(var t = 0; t < this.eventTemp.length; t++){
          this.events.push({
            name: this.eventTemp[t].name,
            start: this.eventTemp[t].start,
            end: this.eventTemp[t].end,
            color: this.getColor(this.eventTemp[t].name),
            timed: true,
          })
        }
      },
        getColor(name){
        for(var i = 0; i<this.names.length;i++){
          if (name==this.names[i]){
            return this.colors[i]
          }
        }

      },
      getEventColor (event) {
        return event.color
      },
    },
    watch:{
      employee:{
        handler(newVal,oldVal){
          // alert("值发生变化"+newVal)
          this.employee = newVal
          this.user_id = this.employee
          this.reload = false
          this.$nextTick(() => {
            this.reload = true
          })
        }
      }
    },
    created(){
      // alert(this.employee)
      this.user_id = this.employee
      var date = new Date()
      this.value = date.getFullYear()+"-" +(date.getMonth()+1)+"-"+date.getDate()

    }
  }
</script>

<style>
.calendar{
  padding: 20px;
}
</style>