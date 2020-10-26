<template>
  <v-container>
    <div class="list">
      <v-data-table :headers="headers" :items="leavelist" sort-by="leave_id" class="elevation-1">
        <template v-slot:top>
          <v-toolbar flat color="white">
            <v-toolbar-title>我的请假草稿箱</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-spacer></v-spacer>
            <v-btn color="primary" dark @click="newLeave">新建请假单</v-btn>
          </v-toolbar>
        </template>
        <template v-slot:item.actions="{ item }">
          <v-icon small class="mr-2" @click="viewItem(item)" color="primary">mdi-magnify-plus</v-icon>
          <v-icon small class="mr-2" @click="editItem(item)" color="primary">mdi-pencil</v-icon>
          <v-icon small @click="deleteItem(item)" color="primary">mdi-delete</v-icon>
        </template>
        <template v-slot:no-data>
          <v-btn color="primary" @click="initialize">重置</v-btn>
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
  </v-container>
</template>

<style>
</style>

<script>
export default {
  data: () => ({
    leaveid: "",
    dialog: false,
    headers: [
      { text: "请假单编号", align: "start", value: "leave_id" },
      { text: "请假开始时间", value: "starttime" },
      { text: "请假结束时间", value: "endtime" },
      { text: "申请提交时间", value: "pushtime" },
      { text: "处理方式", value: "handlemode", sortable: false },
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
      params.append("userid", localStorage.getItem("userid"));
      this.axios
        .post(this.SERVICE_PATH + "leave/draft/initialize", params)
        .then((res) => {
          this.leavelist = res.data.data;
        })
        .catch((err) => {
          console.log(err);
        });
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
      this.$router.push({
        path: "newLeave",
        query: {
          leaveid: item.leave_id,
        },
      });
    },

    deleteItem(item) {
      var params = new URLSearchParams();
      params.append("leave_id", item.leave_id);
      let that = this;
      const index = this.leavelist.indexOf(item);
      if (confirm("确定删除该条请假申请吗？")) {
        this.axios
          .post(this.SERVICE_PATH + "leave/eLeaveList/delete", params)
          .then(function (res) {
            if (res.status == 200) {
              alert("删除成功");
              that.leavelist.splice(index, 1);
            }
          })
          .catch(function (error) {
            console.log(error);
          });
      }
    },

    close() {
      this.dialog = false;
    },
  },
};
</script>