<template>
  <v-container>
    <div class="top_tip">
      <font size="5" style="position: absolute;top: 4%;left: 8%">编辑请假单</font>
    </div>
    <div class="mainbody">
      <v-card outline>
        <div class="startTime">
          <v-row justify="center">
            <v-col md="2" align="end">开始时间：</v-col>

            <v-col cols="12" sm="4" md="3">
              <v-dialog
                ref="startDayDialog"
                v-model="startDayDialog"
                :return-value.sync="startDay"
                persistent
                width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="startDay"
                    label="开始日期"
                    readonly
                    dense
                    :rules="[rules.required]"
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker v-model="startDay" scrollable>
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click=" startDayDialog = false">取消</v-btn>
                  <v-btn text color="primary" @click="  $refs.startDayDialog.save(startDay)">确定</v-btn>
                </v-date-picker>
              </v-dialog>
            </v-col>
            <v-col cols="12" sm="4" md="3">
              <v-dialog
                ref="startTimeDialog"
                v-model="startTimeDialog"
                :return-value.sync="startTime"
                persistent
                width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="startTime"
                    label="选择开始时间"
                    :rules="[rules.required]"
                    dense
                    readonly
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-time-picker v-if="startTimeDialog" v-model="startTime" full-width>
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="startTimeDialog = false">取消</v-btn>
                  <v-btn text color="primary" @click="$refs.startTimeDialog.save(startTime)">确定</v-btn>
                </v-time-picker>
              </v-dialog>
            </v-col>
          </v-row>
        </div>

        <div class="endTime">
          <v-row justify="center">
            <v-col md="2" align="end">结束时间：</v-col>
            <v-col cols="12" sm="4" md="3">
              <v-dialog
                ref="endDayDialog"
                v-model="endDayDialog"
                :return-value.sync="endDay"
                persistent
                width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="endDay"
                    label="选择结束日期"
                    :rules="[rules.required]"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                    dense
                  ></v-text-field>
                </template>
                <v-date-picker v-model="endDay" scrollable>
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click=" endDayDialog = false">Cancel</v-btn>
                  <v-btn text color="primary" @click="  $refs.endDayDialog.save(endDay)">OK</v-btn>
                </v-date-picker>
              </v-dialog>
            </v-col>
            <v-col cols="11" sm="3">
              <v-dialog
                ref="endTimeDialog"
                v-model="endTimeDialog"
                :return-value.sync="endTime"
                persistent
                width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="endTime"
                    label="选择结束时间"
                    dense
                    readonly
                    :rules="[rules.required]"
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-time-picker v-if="endTimeDialog" v-model="endTime" full-width>
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="endTimeDialog = false">取消</v-btn>
                  <v-btn text color="primary" @click="$refs.endTimeDialog.save(endTime)">确定</v-btn>
                </v-time-picker>
              </v-dialog>
            </v-col>
          </v-row>
        </div>
        <div class="reasons">
          <v-row justify="center">
            <v-col md="2" align="end">申请理由：</v-col>
            <v-col cols="12" sm="6">
              <v-textarea
                v-model="reason"
                label="申请理由"
                auto-grow
                outlined
                row-height="25"
                shaped
                :rules="[rules.required]"
              ></v-textarea>
            </v-col>
          </v-row>
        </div>
        <div class="files">
          <v-row justify="center">
            <v-col md="2" align="end">申请证明材料：</v-col>
            <v-col cols="12" sm="6">
              <v-file-input label="上传文件" outlined dense></v-file-input>
            </v-col>
          </v-row>
        </div>
        <div class="urgent">
          <v-row justify="center">
            <v-col md="2" align="end">处理方式：</v-col>
            <v-col cols="12" sm="6">
              <v-radio-group v-model="radio" row :rules="[rules.required]">
                <v-radio label="正常处理" value="1"></v-radio>
                <v-radio label="加急" value="2"></v-radio>
                <v-radio label="特殊申请" value="3"></v-radio>
              </v-radio-group>
            </v-col>
          </v-row>
        </div>
        <div class="btns">
          <v-btn large color="primary" class="ma-2" @click="submit">提交</v-btn>
          <v-btn class="ma-2" @click="cancelNew">取消</v-btn>
          <v-btn class="ma-2" @click="saveToDraft">保存</v-btn>
        </div>
      </v-card>
    </div>
  </v-container>
</template>

<style>
.top_tip {
  background-color: #f0f8ff;
  height: 60px;
}
.btns {
  position: absolute;
  bottom: 5%;
  right: 4%;
}
</style>

<script>
export default {
  data: () => ({
    leaveid: "",
    startDayDialog: false,
    startDay: "",
    startTimeDialog: false,
    startTime: "",
    endDayDialog: false,
    endDay: "",
    endTimeDialog: false,
    endTime: "",
    reason: "",
    files: [],
    radio: "",
    rules: {
      required: (value) => !!value || "必填项",
    },
  }),

  mounted: function () {},

  created() {
    this.leaveid = this.$route.query.leaveid;
    this.initialize();
  },

  methods: {
    initialize() {
      var params = new URLSearchParams();
      if (this.leaveid) {
        params.append("leave_id", this.leaveid);
        this.axios
          .post(this.SERVICE_PATH + "leave/newLeave/find", params)
          .then((res) => {
            this.reason = res.data.data.reason;
            this.startDay = res.data.data.startday;
            this.startTime = res.data.data.starttime;
            this.endDay = res.data.data.endday;
            this.endTime = res.data.data.endtime;
            if (res.data.data.handlemode == "正常处理") {
              this.radio = "1";
            } else if (res.data.data.handlemode == "加急") {
              this.radio = "2";
            } else if (res.data.data.handlemode == "特殊申请") {
              this.radio = "3";
            }
          })
          .catch((err) => {
            console.log(err);
          });
      }
    },

    submit() {
      if (
        this.startDay.length == 0 ||
        this.startTime.length == 0 ||
        this.endDay.length == 0 ||
        this.endTime.length == 0 ||
        this.reason.length == 0 ||
        this.radio.length == 0
      ) {
        alert("请填上所有的必填项");
      } else {
        var startday = this.startDay.split("-");
        var starttime = this.startTime.split(":");
        var start = startday + starttime;
        var endday = this.endDay.split("-");
        var endtime = this.endTime.split(":");
        var end = endday + endtime;
        if (start > end) {
          alert("时间范围有误，开始时间不得大于结束时间");
        } else {
          let that = this;
          var handle = "";
          if (this.radio == "1") {
            handle = "正常处理";
          } else if (this.radio == "2") {
            handle = "加急";
          } else {
            handle = "特殊申请";
          }
          var params = new URLSearchParams();
          params.append("userid", localStorage.getItem("userid"));
          params.append("startDay", this.startDay);
          params.append("startTime", this.startTime);
          params.append("endDay", this.endDay);
          params.append("endTime", this.endTime);
          params.append("reason", this.reason);
          params.append("handle", handle);
          params.append("leaveid", this.leaveid);

          if (this.leaveid) {
            this.axios
              .post(this.SERVICE_PATH + "leave/update", params)
              .then(function (res) {
                if (res.status == 200) {
                  alert("提交成功");
                  that.$router.push({ path: "LeaveList_e" });
                }
              })
              .catch(function (error) {
                console.log(error);
              });
          } else {
            this.axios
              .post(this.SERVICE_PATH + "leave/new", params)
              .then(function (res) {
                if (res.status == 200) {
                  alert("提交成功");
                  that.$router.push({ path: "LeaveList_e" });
                }
              })
              .catch(function (error) {
                console.log(error);
              });
          }
        }
      }
    },

    cancelNew() {
      this.startDay = "";
      this.startTime = "";
      this.endDay = "";
      this.endTime = "";
      this.reason = "";
      this.radio = "";
    },

    //保存
    saveToDraft() {
      var handle = "";
      let that = this;
      if (this.radio == "1") {
        handle = "正常处理";
      } else if (this.radio == "2") {
        handle = "加急";
      } else if (this.radio == "3") {
        handle = "特殊申请";
      }

      var params = new URLSearchParams();
      params.append("userid", localStorage.getItem("userid"));
      params.append("startDay", this.startDay);
      params.append("startTime", this.startTime);
      params.append("endDay", this.endDay);
      params.append("endTime", this.endTime);
      params.append("reason", this.reason);
      params.append("handle", handle);
      params.append("leaveid", this.leaveid);

      if (this.leaveid) {
        this.axios
          .post(this.SERVICE_PATH + "leave/updatetodraft", params)
          .then(function (res) {
            console.log(res.data);
            if (res.status == 200) {
              alert("提交成功");
              that.$router.push({ path: "LeaveDraft" });
            }
          })
          .catch(function (error) {
            console.log(error);
          });
      } else {
        this.axios
          .post(this.SERVICE_PATH + "leave/save", params)
          .then(function (res) {
            console.log(res.data);
            if (res.status == 200) {
              alert("提交成功");
              that.$router.push({ path: "LeaveDraft" });
            }
          })
          .catch(function (error) {
            console.log(error);
          });
      }
    },
  },
};
</script>