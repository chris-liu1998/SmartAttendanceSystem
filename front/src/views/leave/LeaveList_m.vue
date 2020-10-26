<template>
  <v-container>
    <div class="topinfo">
      <font size="5">请假处理</font>
    </div>
    <div class="searchbar">
      <v-row>
        <v-col cols="12" sm="4" md="2">
          <v-menu
            ref="menu"
            v-model="menu"
            :close-on-content-click="false"
            :return-value.sync="searchday"
            transition="scale-transition"
            offset-y
            min-width="290px"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field v-model="searchday" label="选择日期" readonly v-bind="attrs" v-on="on"></v-text-field>
            </template>
            <v-date-picker v-model="searchday" no-title scrollable>
              <v-spacer></v-spacer>
              <v-btn text color="primary" @click="menu = false">取消</v-btn>
              <v-btn text color="primary" @click="$refs.menu.save(searchday)">确认</v-btn>
            </v-date-picker>
          </v-menu>
        </v-col>
        <v-col cols="12" sm="3">
          <v-text-field v-model="searchid" label="请输入员工工号" append-icon="mdi-magnify"></v-text-field>
        </v-col>
        <v-col class="d-flex" cols="12" sm="2">
          <v-select :items="handleitems" label="紧急状态" outlined dense v-model="searchhandle"></v-select>
        </v-col>
        <v-col class="d-flex" cols="12" sm="2">
          <v-select :items="stateitems" label="处理状态" outlined dense v-model="searchstate"></v-select>
        </v-col>
        <v-col class="d-flex" cols="12" sm="2">
          <v-btn color="primary" @click="search">检索</v-btn>
        </v-col>
      </v-row>
    </div>

    <div class="list">
      <v-chip class="ma-2" color="primary" label large outlined>
        <v-icon left>mdi-label</v-icon>
        <div>
          共搜索到
          <font color="#EE6A50">{{ count }}</font>条请假记录。
          <br />其中
          <font color="#EE6A50">{{ doingcount }}</font>条请假记录尚未批阅，快去看看吧！
        </div>
      </v-chip>
      <div class="list_info">
        <v-data-table :headers="headers" :items="leavelist" sort-by="leaveid" class="elevation-1">
          <template v-slot:top>
            <v-toolbar flat color="white">
              <v-toolbar-title>请假列表</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
            </v-toolbar>
          </template>
          <template v-slot:item.actions="{ item }">
            <v-icon small class="mr-2" @click="viewItem(item)" color="primary">mdi-magnify-plus</v-icon>
            <v-btn text small color="primary" @click="agree(item)" v-if="item.processmode=='审核中'">同意</v-btn>
            <v-btn
              text
              small
              color="primary"
              @click="reject(item)"
              v-if="item.processmode=='审核中'"
            >驳回</v-btn>
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
</style>

<script>
export default {
  data: () => ({
    count: "",
    doingcount: "",

    searchday: "",
    searchid: "",
    searchhandle: "",
    searchstate: "",

    handleitems: ["正常处理", "加急", "特殊申请"],
    stateitems: ["审核中", "已通过", "未通过"],
    menu: false,
    dialog: false,
    headers: [
      { text: "请假单编号", align: "start", value: "leave_id" },
      { text: "申请人姓名", value: "employee_name", sortable: false },
      { text: "申请人工号", value: "employee_id" },
      { text: "申请人部门", value: "department_name", sortable: false },
      { text: "紧急状态", value: "handlemode", sortable: false },
      { text: "请假开始时间", value: "starttime" },
      { text: "请假结束时间", value: "endtime" },
      { text: "申请提交时间", value: "pushtime" },
      { text: "当前状态", value: "processmode", sortable: false },
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
  }),

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
      params.append("flag", localStorage.getItem("flag"));
      params.append("userid", localStorage.getItem("userid"));

      this.axios
        .post(this.SERVICE_PATH + "leave/manage/initialize", params)
        .then((res) => {
          this.count = res.data.data.leaveNum;
          this.doingcount = res.data.data.doingNum;
          this.leavelist = res.data.data.mess;
        })
        .catch((err) => {
          console.log(err);
        });
    },

    viewItem(item) {
      this.editedIndex = this.leavelist.indexOf(item);
      console.log(item);
      this.viewedItem = item;
      this.dialog = true;
    },

    close() {
      this.dialog = false;
    },

    agree(item) {
      var params = new URLSearchParams();
      params.append("leaveid", item.leave_id);
      params.append("processmode", "已通过");

      if (confirm("确定批准该请假申请吗？")) {
        this.axios
          .post(this.SERVICE_PATH + "leave/manage/handle", params)
          .then(function (res) {
            if (res.status == 200) {
              alert("操作成功");
              item.processmode = "已通过";
            }
          })
          .catch(function (error) {
            console.log(error);
          });
      }
    },

    //驳回
    reject(item) {
      var params = new URLSearchParams();
      params.append("leaveid", item.leave_id);
      params.append("processmode", "未通过");

      if (confirm("确定拒绝该请假申请吗？")) {
        this.axios
          .post(this.SERVICE_PATH + "leave/manage/handle", params)

          .then(function (res) {
            if (res.status == 200) {
              alert("操作成功");
              item.processmode = "未通过";
            }
          })
          .catch(function (error) {
            console.log(error);
          });
      }
    },

    //搜索，done
    search() {
      var params = new URLSearchParams();
      params.append("flag", localStorage.getItem("flag"));
      params.append("userid", localStorage.getItem("userid"));
      params.append("date", this.searchday);
      params.append("searchid", this.searchid);
      params.append("searchhandlemode", this.searchhandle);
      params.append("searchprocessmode", this.searchstate);

      let that = this;

      this.axios
        .post(this.SERVICE_PATH + "leave/manage/search", params)
        .then(function (res) {
          that.leavelist = res.data.data.mess;
          that.count = res.data.data.LeaveNum;
          that.doingcount = res.data.data.doingNum;
        })
        .catch(function (error) {
          console.log(error);
        });
    },
  },
};
</script>