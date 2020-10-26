<template>
  <v-container fulid>
    <div class="mainbody">
      <v-card outline color="deep-purple lighten-5" id="newItem">
        <v-list-item two-line>
          <v-list-item-content>
            <v-list-item-title class="headline">新增考勤设置</v-list-item-title>
            <v-list-item-subtitle>请输入考勤信息</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-card>
          <div class="Date">
            <v-row justify="center">
              <v-col md="2" align="end" style="margin-top:7px">指定日期范围：</v-col>

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
                      label="选择开始日期"
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
                    <v-btn text color="primary" @click=" endDayDialog = false">取消</v-btn>
                    <v-btn text color="primary" @click="  $refs.endDayDialog.save(endDay)">确定</v-btn>
                  </v-date-picker>
                </v-dialog>
              </v-col>
            </v-row>
          </div>

          <div class="Time">
            <v-row justify="center">
              <v-col md="2" align="end" style="margin-top:7px">指定打卡时间：</v-col>
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

          <div>
            <v-row justify="center">
              <v-col cols="12" md="2" align="end" style="margin-top:20px">每周重复：</v-col>
              <v-col cols="12" md="3" style="margin-top:-10px">
                <v-row style="height:50px">
                  <v-col cols="12" md="6">
                    <v-checkbox v-model="week_checkbox[0]" :label="`周一`"></v-checkbox>
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-checkbox v-model="week_checkbox[1]" :label="`周二`"></v-checkbox>
                  </v-col>
                </v-row>
              </v-col>

              <v-col cols="12" md="3" style="margin-top:-10px">
                <v-row style="height:50px">
                  <v-col cols="12" md="6">
                    <v-checkbox v-model="week_checkbox[2]" :label="`周三`"></v-checkbox>
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-checkbox v-model="week_checkbox[3]" :label="`周四`"></v-checkbox>
                  </v-col>
                </v-row>
              </v-col>
            </v-row>

            <v-row justify="center">
              <v-col cols="12" md="2" align="end" style="margin-top:8px"></v-col>
              <v-col cols="12" md="3">
                <v-row style="height:50px">
                  <v-col cols="12" md="6">
                    <v-checkbox v-model="week_checkbox[4]" :label="`周五`"></v-checkbox>
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-checkbox v-model="week_checkbox[5]" :label="`周六`"></v-checkbox>
                  </v-col>
                </v-row>
              </v-col>

              <v-col cols="12" md="3">
                <v-row style="height:50px">
                  <v-col cols="12" md="6">
                    <v-checkbox v-model="week_checkbox[6]" :label="`周日`"></v-checkbox>
                  </v-col>

                  <v-col cols="12" md="6"></v-col>
                </v-row>
              </v-col>
            </v-row>
          </div>

          <div class="Date">
            <v-row justify="center">
              <v-col md="2" align="end" style="margin-top:7px">弹性时间：</v-col>

              <v-col cols="12" sm="4" md="3">
                <v-text-field v-model="elastic_time" label="单位: 分钟" dense></v-text-field>
              </v-col>
              <v-col cols="12" sm="4" md="3"></v-col>
            </v-row>
          </div>
          <div class="Date">
            <v-row justify="center">
              <v-col md="2" align="end" style="margin-top:7px"></v-col>

              <v-col cols="12" sm="4" md="3">
                <v-btn color="info" class="ma-2" @click="submit">
                  <h3>提交</h3>
                </v-btn>
                <v-btn color="info" class="ma-2" @click="cancelNew">
                  <h3>重置</h3>
                </v-btn>
              </v-col>
              <v-col cols="12" sm="4" md="3"></v-col>
            </v-row>
          </div>
        </v-card>
      </v-card>
    </div>

    <div class="mainbody" style="margin-top:30px">
      <v-card outline color="deep-purple lighten-5">
        <v-list-item two-line>
          <v-list-item-content>
            <v-list-item-title class="headline">考勤设定列表</v-list-item-title>
            <v-list-item-subtitle></v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-data-table :headers="headers" :items="desserts" sort-by="id" class="elevation-1">
          <template v-slot:top>
            <v-toolbar flat color="white">
              <v-toolbar-title>列表一览</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-dialog v-model="dialog" max-width="800px">
                <v-card>
                  <v-card-title>
                    <span class="headline">{{ formTitle }}</span>
                  </v-card-title>

                  <v-card-text>
                    <v-container>
                      <v-row>
                        <v-col cols="12" sm="6" md="4">
                          <v-dialog
                            ref="startDayDialog"
                            v-model="startDayDialog"
                            :return-value.sync="startDay"
                            persistent
                            width="290px"
                          >
                            <template v-slot:activator="{ on, attrs }">
                              <v-text-field
                                v-model="editedItem.dateStart"
                                label="选择开始日期"
                                readonly
                                dense
                                :rules="[rules.required]"
                                v-bind="attrs"
                                v-on="on"
                              ></v-text-field>
                            </template>
                            <v-date-picker v-model="editedItem.dateStart" scrollable>
                              <v-spacer></v-spacer>
                              <v-btn text color="primary" @click="startDayDialog = false ">确定</v-btn>
                            </v-date-picker>
                          </v-dialog>
                        </v-col>

                        <v-col cols="12" sm="6" md="6">
                          <v-dialog
                            ref="endDayDialog"
                            v-model="endDayDialog"
                            :return-value.sync="endDay"
                            persistent
                            width="290px"
                          >
                            <template v-slot:activator="{ on, attrs }">
                              <v-text-field
                                v-model="editedItem.dateEnd"
                                label="选择结束日期"
                                :rules="[rules.required]"
                                readonly
                                v-bind="attrs"
                                v-on="on"
                                dense
                              ></v-text-field>
                            </template>
                            <v-date-picker v-model="editedItem.dateEnd" scrollable>
                              <v-spacer></v-spacer>
                              <v-btn text color="primary" @click=" endDayDialog = false">确定</v-btn>
                            </v-date-picker>
                          </v-dialog>
                        </v-col>
                        <v-col cols="12" sm="6" md="6">
                          <v-dialog
                            ref="startTimeDialog"
                            v-model="startTimeDialog"
                            :return-value.sync="startTime"
                            persistent
                            width="290px"
                          >
                            <template v-slot:activator="{ on, attrs }">
                              <v-text-field
                                v-model="editedItem.timeStart"
                                label="选择开始时间"
                                :rules="[rules.required]"
                                dense
                                readonly
                                v-bind="attrs"
                                v-on="on"
                              ></v-text-field>
                            </template>
                            <v-time-picker
                              v-if="startTimeDialog"
                              v-model="editedItem.timeStart"
                              full-width
                            >
                              <v-spacer></v-spacer>
                              <v-btn text color="primary" @click="startTimeDialog = false">确定</v-btn>
                            </v-time-picker>
                          </v-dialog>
                        </v-col>
                        <v-col cols="12" sm="6" md="6">
                          <v-dialog
                            ref="endTimeDialog"
                            v-model="endTimeDialog"
                            :return-value.sync="endTime"
                            persistent
                            width="290px"
                          >
                            <template v-slot:activator="{ on, attrs }">
                              <v-text-field
                                v-model="editedItem.timeEnd"
                                label="选择结束时间"
                                dense
                                readonly
                                :rules="[rules.required]"
                                v-bind="attrs"
                                v-on="on"
                              ></v-text-field>
                            </template>
                            <v-time-picker
                              v-if="endTimeDialog"
                              v-model="editedItem.timeEnd"
                              full-width
                            >
                              <v-spacer></v-spacer>
                              <v-btn text color="primary" @click="endTimeDialog = false">确定</v-btn>
                            </v-time-picker>
                          </v-dialog>
                        </v-col>
                        <v-col cols="12" sm="6" md="6">
                          <v-text-field v-model="editedItem.elasticTime" label="弹性时间"></v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6" md="6">
                          <v-text-field v-model="editedItem.weekDays" label="每周时间"></v-text-field>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="close">取消</v-btn>
                    <v-btn color="blue darken-1" text @click="updateAtt">确定</v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-toolbar>
          </template>

          <!--表格操作-->
          <template v-slot:item.actions="{ item }">
            <v-icon small color="green" class="mr-2" @click="editItem(item)">mdi-pencil</v-icon>
            <v-icon small color="red" class="mr-2" @click="deleteItem(item)">mdi-delete</v-icon>
            <v-icon small color="blue" @click="activateItem(item)">mdi-access-point</v-icon>
          </template>
          <template v-slot:item.state="{ item }">
            <!--这里Eslint报错无所谓-->
            <v-chip :color="getColor(item.state)" dark>{{ item.state }}</v-chip>
          </template>
          <template v-slot:no-data>
            <v-btn color="primary" @click="initialize">刷新</v-btn>
          </template>
        </v-data-table>
      </v-card>
    </div>
  </v-container>
</template>


<script>
export default {
  data: () => ({
    startDayDialog: false,
    startDay: "",
    endDayDialog: false,
    endDay: "",

    startTimeDialog: false,
    startTime: "",
    endTimeDialog: false,
    endTime: "",

    week_checkbox: [false, false, false, false, false, false, false],

    elastic_time: "",

    rules: {
      required: value => !!value || "必填项"
    },
    dialog: false,
    headers: [
      {
        text: "序号",
        align: "start",
        value: "id"
      },
      { text: "起止日期", value: "dateDelta", sortable: false },
      { text: "起止时间", value: "timeDelta", sortable: false },
      { text: "弹性时间(分钟)", value: "elasticTime", sortable: false },
      { text: "每周（周一-周日）", value: "weekDays", sortable: false },
      { text: "使用状态", value: "state", sortable: false },
      { text: "操 作", value: "actions", sortable: false }
    ],
    desserts: [],
    editedIndex: -1,
    editedItem: {
      id: 0,
      dateDelta: "",
      timeDelta: "",
      elasticTime: "",
      weekDays: "",

      dateStart: "",
      dateEnd: "",
      timeStart: "",
      timeEnd: ""
    }
  }),
  computed: {
    formTitle() {
      return "编辑设置";
    }
  },
  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  mounted() {
    this.initialize();
  },

  methods: {
    // inject: ["reload"],
    //初始化，获取表格数据

    getColor(state) {
      if (state == "已激活"){
        return "green lighten-2"
      }
      else{
        return "grey"
      }
    },

    initialize() {
      this.axios.get(this.SERVICE_PATH + "attsettinglist").then(res => {
        this.desserts = res.data.data;
      });
    },
    editItem(item) {
      this.editedItem.id = item.id;
      var date = item.dateDelta.split("/");
      var time = item.timeDelta.split("-");
      this.editedItem = Object.assign({}, item);
      this.editedItem.dateStart = date[0];
      this.editedItem.dateEnd = date[1];
      this.editedItem.timeStart = time[0];
      this.editedItem.timeEnd = time[1];
      this.dialog = true;
    },
    deleteItem(item) {
      let id = item.id;
      if (confirm("删除后无法还原，确认删除？")) {
        //删除请求
        let params = new URLSearchParams();
        params.append("id", id);
        this.axios
          .post(this.SERVICE_PATH + "deleteattsetting ", params)
          .then(res => {
            // alert(res.data.data);
            if (res.status == 200) {
              alert("删除成功！");
              this.initialize();
              // this.reload();
            }
          });
      }
    },

    activateItem(item) {
      this.axios
        .post(this.SERVICE_PATH + "department/attendsetting", "", {
          params: { setting_id: item.id }
        })
        .then(res => {
          if (res.data.code === 0) {
            item.state = "已激活";
            alert("激活成功！");
            this.initialize();
          } else {
            alert("激活失败！");
            this.initialize();
          }
        });
    },
    close() {
      this.dialog = false;
    },
    updateAtt() {
      //添加post方法传递数据,申请修改
      var params = new URLSearchParams();
      params.append("id", this.editedItem.id);
      params.append("startDay", this.editedItem.dateStart);
      params.append("endDay", this.editedItem.dateEnd);
      params.append("startTime", this.editedItem.timeStart);
      params.append("endTime", this.editedItem.timeEnd);
      params.append("weekDays", this.editedItem.weekDays);
      params.append("elasticTime", this.editedItem.elasticTime);

      this.axios
        .post(this.SERVICE_PATH + "updateattsetting ", params)
        .then(res => {
          // alert(res.data.data);
          if (res.status == 200) {
            alert("更新成功！");
            this.initialize();
            this.cancelNew();
          }
        });

      this.close();
    },
    submit() {
      var params = new URLSearchParams();
      var week_days = this.transWeekDays();
      // alert(week_days);
      if (
        this.startDay &&
        this.endDay &&
        week_days &&
        this.startTime &&
        this.endTime
      ) {
        params.append("startDay", this.startDay);
        params.append("endDay", this.endDay);
        params.append("startTime", this.startTime);
        params.append("endTime", this.endTime);
        params.append("weekDays", week_days);
        params.append("elasticTime", this.elastic_time);
        this.axios
          .post(this.SERVICE_PATH + "newattsetting", params)
          .then(res => {
            // alert(res.data.data);
            if (res.status == 200) {
              alert("设置成功！");
              this.initialize();
              this.cancelNew();
            }
          });
      } else {
        alert("请完整填写设置！");
      }
    },
    transWeekDays() {
      var temp = "";
      for (var i = 0; i < this.week_checkbox.length; i++) {
        if (this.week_checkbox[i] == true) {
          temp += "1/";
        } else {
          temp += "0/";
        }
      }

      temp = temp.slice(0, temp.length - 1);
      console.log(temp);
      return temp;
    },
    cancelNew() {
      (this.startDayDialog = false),
        (this.startDay = ""),
        (this.endDayDialog = false),
        (this.endDay = ""),
        (this.startTimeDialog = false),
        (this.startTime = ""),
        (this.endTimeDialog = false),
        (this.endTime = ""),
        (this.week_checkbox = [
          false,
          false,
          false,
          false,
          false,
          false,
          false
        ]),
        (this.elastic_time = "");
    }
  }
};
</script>

<style>
.top_tip {
  background-color: #f0f8ff;
  height: 60px;
}
.btns {
  position: absolute;
  /* buttom: 5%; */
  right: 4%;
}
</style>
