<template>
  <v-container>
    <div class="searchbar">
      <v-row>
        <v-col cols="12" sm="4" md="3">
          <v-menu
            ref="menu"
            v-model="menu"
            :close-on-content-click="false"
            :return-value.sync="date"
            transition="scale-transition"
            offset-y
            min-width="290px"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field v-model="date" label="选择日期" readonly v-bind="attrs" v-on="on"></v-text-field>
            </template>
            <v-date-picker v-model="date" no-title scrollable>
              <v-spacer></v-spacer>
              <v-btn text color="primary" @click="menu = false">取消</v-btn>
              <v-btn text color="primary" @click="$refs.menu.save(date)">确认</v-btn>
            </v-date-picker>
          </v-menu>
        </v-col>
        <!--
                <v-col cols="12" sm="3">
                    <v-text-field v-model="searchinfo" solo label="请输入关键字" clearable></v-text-field>
                </v-col>
        -->
        <v-col cols="12" sm="6">
          <v-btn rounded color="primary" dark style="top: 5px" @click="search">搜索</v-btn>
        </v-col>
      </v-row>
    </div>

    <div class="list">
      <v-chip class="ma-2" color="primary" label large outlined>
        <v-icon left>mdi-label</v-icon>
        <div>
          共搜索到
          <font color="#EE6A50">{{ count }}</font>条请假记录。
          <br />已批准
          <font color="#EE6A50">{{ passcount }}</font>条，已驳回
          <font color="#EE6A50">{{ rejectcount }}</font>条，待审核
          <font color="#EE6A50">{{ doingcount }}</font>条，请及时调整未通过的请假申请，以免影响考勤。
        </div>
      </v-chip>
      <div class="list_info">
        <v-data-table :headers="headers" :items="leavelist" sort-by="leaveid" class="elevation-1">
          <template v-slot:top>
            <v-toolbar flat color="white">
              <v-toolbar-title>我的请假列表</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <v-btn color="primary" dark @click="newLeave">新建请假单</v-btn>
            </v-toolbar>
          </template>
          <template v-slot:item.actions="{ item }">
            <v-icon small class="mr-2" @click="viewItem(item)" color="primary">mdi-magnify-plus</v-icon>
            <v-icon
              small
              class="mr-2"
              @click="editItem(item)"
              color="primary"
              v-if="item.processmode=='审核中'||item.processmode=='未通过'"
            >mdi-pencil</v-icon>
            <v-icon
              small
              @click="deleteItem(item)"
              color="primary"
              v-if="item.processmode=='审核中'||item.processmode=='未通过'"
            >mdi-delete</v-icon>
            <!-- <v-icon small class="mr-2" v-if="item.processmode=='已通过'">mdi-pencil</v-icon>
            <v-icon small v-if="item.processmode=='已通过'">mdi-delete</v-icon> -->
          </template>
        </v-data-table>
        <v-dialog v-model="dialog" max-width="500px">
          <v-card>
            <v-card-title>
              <span class="headline">请假单详情</span>
            </v-card-title>
            <v-card-text>
              <v-container>
                <div>请假起止时间： {{ viewedItem.starttime }} - {{ viewedItem.endtime }}</div>
                <div>请假理由： {{ viewedItem.reason }}</div>
                <div>处理方式： {{ viewedItem.handlemode }}</div>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="close">关闭</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </div>
    </div>
  </v-container>
</template>

<style>
.searchbtn {
  position: absolute;
  top: 66%;
}
</style>

<script>
export default {
  data: () => ({
    date: "",
    searchinfo: "",

    count: "",
    doingcount: "",
    passcount: "",
    rejectcount: "",

    dialog: false,
    headers: [
      { text: "请假单编号", align: "start", value: "leave_id" },
      { text: "请假开始时间", value: "starttime" },
      { text: "请假结束时间", value: "endtime" },
      { text: "申请提交时间", value: "pushtime" },
      { text: "当前状态", value: "processmode", sortable: false },
      { text: "处理时间", value: "handletime" },
      { text: "操作", value: "actions", sortable: false },
    ],
    leavelist: [],

    editedIndex: -1,
    viewedItem: {
      leave_id: "",
      starttime: "",
      endtime: "",
      reason: "",
      handlemode: "",
    },
    menu: false,
  }),

  computed: {},

  watch: {
    dialog(val) {
      val || this.close();
    },
  },

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      var params = new URLSearchParams();
      params.append("userid", localStorage.getItem("userid"));
      this.axios
        .post(this.SERVICE_PATH + "leave/eLeaveList/initialize", params)
        .then((res) => {
          this.leavelist = res.data.data.mess;
          this.count = res.data.data.leaveNum;
          this.doingcount = res.data.data.doingNum;
          this.passcount = res.data.data.passNum;
          this.rejectcount = res.data.data.rejectedNum;
        })
        .catch((err) => {
          console.log(err);
        });
    },

    search() {
      var params = new URLSearchParams();
      params.append("userid", localStorage.getItem("userid"));
      params.append("date", this.date);

      let that = this;
      if (this.date == "") {
        alert("请输入需要查询的日期");
      } else {
        this.axios
          .post(this.SERVICE_PATH + "leave/eLeaveList/search", params)
          .then(function (res) {
            that.leavelist = res.data.data.mess;
            that.count = res.data.data.LeaveNum;
            that.doingcount = res.data.data.doingNum;
            that.passcount = res.data.data.passNum;
            that.rejectcount = res.data.data.rejectedNum;
          })
          .catch(function (error) {
            console.log(error);
          });
      }
    },

    newLeave() {
      this.$router.push({
        path: "newLeave",
      });
    },

    viewItem(item) {
      this.editedIndex = this.leavelist.indexOf(item);
      console.log(item);
      this.viewedItem = item;
      this.dialog = true;
    },

    editItem(item) {
      console.log(item.leave_id);
      this.$router.push({
        path: "newLeave",
        query: {
          leaveid: item.leave_id,
        },
      });
    },

    deleteItem(item) {
      var params = new URLSearchParams();
      params.append("leave_id", this.viewedItem.leave_id);

      let that = this;
      var thisstate = item.state;
      const index = this.leavelist.indexOf(item);
      if (confirm("确定删除该条请假申请吗？")) {
        this.axios
          .post(this.SERVICE_PATH + "leave/eLeaveList/delete", params)
          .then(function (res) {
            if (res.status == 200) {
              alert("删除成功");
              that.leavelist.splice(index, 1);
              that.count--;
              if (thisstate == "未通过") {
                that.rejectcount--;
              } else {
                that.doingcount--;
              }
            }
          })
          .catch(function (error) {
            console.log(error);
          });
      }
    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },
  },
};
</script>