<template>
  <v-container id="user-profile" fluid>
    <v-row justify="center" style="margin-top:40px">
      <v-col cols="12" md="1"></v-col>
      <v-col cols="12" md="8">
        <v-card>
          <v-list-item two-line>
            <v-list-item-content>
              <v-list-item-title class="headline">个人信息</v-list-item-title>
              <v-list-item-subtitle></v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-card-text>
            <v-form>
              <v-container class="py-0">
                <v-row>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="employeeInfo.employee_id"
                      label="工号"
                      class="purple-input"
                      readonly
                    />
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="employeeInfo.employee_name"
                      label="姓名"
                      class="purple-input"
                      readonly
                    />
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="employeeInfo.employee_title"
                      label="职务"
                      class="purple-input"
                      readonly
                    />
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="employeeInfo.department_id"
                      label="所属部门"
                      class="purple-input"
                      readonly
                    />
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="employeeInfo.leader_id"
                      label="直属领导"
                      class="purple-input"
                      readonly
                    />
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="employeeInfo.phone"
                      label="联系电话"
                      class="purple-input"
                      type="phone"
                      readonly
                    />
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="employeeInfo.qq"
                      label="QQ"
                      class="purple-input"
                      readonly
                    />
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="employeeInfo.wechat"
                      label="微信"
                      class="purple-input"
                      readonly
                    />
                  </v-col>
                  <v-col cols="12" class="text-right" @click="updateInfo">
                    <v-btn color="info" class="mr-0">更新个人信息</v-btn>
                  </v-col>

                  <!--编辑对话框-->
                  <v-dialog v-model="dialog" max-width="500px">
                    <v-card>
                      <v-card-title>
                        <span class="headline">更新个人信息</span>
                      </v-card-title>
                      <v-card-text>
                        <v-container>
                          <v-row>
                            <v-col cols="12" sm="6" md="4">
                              <v-text-field v-model="employeeInfo.employee_id" label="工号"></v-text-field>
                            </v-col>
                            <v-col cols="12" sm="6" md="4">
                              <v-text-field v-model="employeeInfo.employee_name" label="姓名"></v-text-field>
                            </v-col>
                            <v-col cols="12" sm="6" md="4">
                              <v-text-field v-model="employeeInfo.employee_title" label="职务"></v-text-field>
                            </v-col>
                            <v-col cols="12" sm="6" md="4">
                              <v-text-field v-model="employeeInfo.department_id" label="所属部门"></v-text-field>
                            </v-col>
                            <v-col cols="12" sm="6" md="4">
                              <v-text-field v-model="employeeInfo.leader_id" label="直属领导"></v-text-field>
                            </v-col>
                            <v-col cols="12" sm="6" md="4">
                              <v-text-field v-model="employeeInfo.phone" label="联系电话"></v-text-field>
                            </v-col>
                            <v-col cols="12" sm="6" md="4">
                              <v-text-field v-model="employeeInfo.qq" label="QQ"></v-text-field>
                            </v-col>
                            <v-col cols="12" sm="6" md="4">
                              <v-text-field v-model="employeeInfo.wechat" label="微信"></v-text-field>
                            </v-col>
                          </v-row>
                        </v-container>
                      </v-card-text>

                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="blue darken-1" text @click="close">取消</v-btn>
                        <v-btn color="blue darken-1" text @click="save">保存</v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                </v-row>
              </v-container>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="2">
        <v-card>
          <v-img class="align-end" height="200px" :src="imgurl" alt="头像" />
          <v-card-text class="text-center">
            <p class="dispplay-2 font-weight-light black--text">账号：{{account}}</p>
            <p class="dispplay-2 font-weight-light black--text">账户类型：{{acccountInfo.flag}}</p>
            <v-file-input
              justify="center"
              v-model="fileInfo"
              show-size
              prepend-icon="mdi-camera"
              accept="image/*"
              label="点击更换头像"
              @change="updateavatar"
            />
            <v-btn color="info" rounded class="mr-0" @click="updatepwd">重置密码</v-btn>
            <!--重置密码对话框-->
            <v-dialog v-model="dialogupdatepwd" max-width="500px">
              <v-card>
                <v-card-title>
                  <span class="headline">重置密码</span>
                </v-card-title>
                <v-card-text>
                  <v-container>
                    <v-row>
                      <v-col cols="12">
                        <v-text-field v-model="oldpwd" label="请输入旧密码"></v-text-field>
                      </v-col>
                      <v-col cols="12">
                        <v-text-field v-model="newpwd" label="请输入新密码"></v-text-field>
                      </v-col>
                      <v-col cols="12">
                        <v-text-field v-model="confirmpwd" label="请再次输入新密码"></v-text-field>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="pwdclose">取消</v-btn>
                  <v-btn color="blue darken-1" text @click="pwdsave">保存</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="1"></v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  // 注入依赖
  inject: ["reload"],
  data() {
    return {
      //是否打开对话框
      dialog: false,
      dialogupdatepwd: false,

      imgurl: null,
      account: "", // localStorage.getItem('userid')
      fileInfo: null,

      employeeInfo: {},
      acccountInfo: {},

      confirmpwd: null,
      oldpwd: null,
      newpwd: null,
    };
  },

  methods: {
    //更换头像
    updateavatar() {
      console.log(this.fileInfo);
      let param = new FormData();
      param.append("avatar", this.fileInfo);
      param.append("account", this.account);
      //axios传输头像到后台
      var avatarurl = this.SERVICE_PATH + "account/avatar";
      this.axios
        .post(avatarurl, param, {
          headers: {
            "Content-Type": "application/form-data",
          },
        })
        .then((res) => {
          if (res.data.code == 200) {
            //刷新页面
            this.reload();
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    //重置密码
    updatepwd() {
      this.dialogupdatepwd = true;
    },
    //更新个人信息
    updateInfo() {
      this.dialog = true;
    },
    pwdclose() {
      this.dialogupdatepwd = false;
    },
    pwdsave() {
      if (this.acccountInfo.password == this.oldpwd) {
        if (this.newpwd == this.confirmpwd) {
          let pwdturl = this.SERVICE_PATH + "account/updatepwd";
          let pwdFormData = new FormData();
          pwdFormData.append("account", this.account);
          pwdFormData.append("password", this.newpwd);
          this.axios
            .post(pwdturl, pwdFormData, {
              headers: {
                "Content-Type": "application/x-www-form-urlencoded",
              },
            })
            .then((res) => {
              //console.log(res.data)
              if (res.data.code == 200) {
                alert("密码重置成功");
                //刷新页面
                this.reload();
              } else if (res.data.code == 201) {
                alert("密码重置失败");
              } else if (res.data.code == 202) {
                alert(res.data.data);
              } else {
                console.log();
              }
            })
            .catch((err) => {
              console.log(err);
            });
        } else {
          alert("两次新密码输入不相同");
        }
      } else {
        alert("旧密码输入错误");
      }
      this.pwdclose();
    },
    close() {
      this.dialog = false;
    },
    save() {
      // 工号、姓名、职务、所属部门都不能为空
      if (
        this.employeeInfo.employee_id != "" &&
        this.employeeInfo.employee_name != "" &&
        this.employeeInfo.employee_title != "" &&
        this.employeeInfo.department_id != ""
      ) {
        // 关闭对话框
        this.dialog = false;
        // 向后台传输数据
        let editurl = this.SERVICE_PATH + "employee/update";
        let employeeFormData = new FormData();
        employeeFormData.append("employee_id", this.employeeInfo.employee_id);
        employeeFormData.append(
          "employee_name",
          this.employeeInfo.employee_name
        );
        employeeFormData.append(
          "employee_title",
          this.employeeInfo.employee_title
        );
        employeeFormData.append(
          "department_name",
          this.employeeInfo.department_id == null
            ? ""
            : this.employeeInfo.department_id
        );
        employeeFormData.append(
          "leader_id",
          this.employeeInfo.leader_id == null ? "" : this.employeeInfo.leader_id
        );
        employeeFormData.append(
          "phone",
          this.employeeInfo.phone == null ? "" : this.employeeInfo.phone
        );
        employeeFormData.append(
          "qq",
          this.employeeInfo.qq == null ? "" : this.employeeInfo.qq
        );
        employeeFormData.append(
          "wechat",
          this.employeeInfo.wechat == null ? "" : this.employeeInfo.wechat
        );
        this.axios
          .post(editurl, employeeFormData, {
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
            },
          })
          .then((res) => {
            //console.log(res.data)
            if (res.data.code == 200) {
              alert("员工" + this.account + "的基本信息更新成功");
              //刷新页面
              this.reload();
            } else if (res.data.code == 201) {
              alert("员工" + this.account + "的基本信息更新失败");
            } else if (res.data.code == 202) {
              alert(res.data.data);
            } else {
              console.log();
            }
          })
          .catch((err) => {
            console.log(err);
          });
      } else {
        alert("工号、姓名、职务都不能为空");
      }
      this.close();
    },
  },
  beforeMount() {
    this.account = localStorage.getItem("userid");
  },
  mounted() {
    //获取头像
    this.imgurl =
      "https://demos.creative-tim.com/vue-material-dashboard/img/marc.aba54d65.jpg";

    //axios获取个人信息
    var employeeoneurl = this.SERVICE_PATH + "employee/one";
    var eidFormData = new FormData();
    eidFormData.append("employee_id", this.account);
    this.axios
      .post(employeeoneurl, eidFormData, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      })
      .then((res) => {
        //console.log(res.data)
        if (res.data.code == 200) {
          this.employeeInfo = res.data.data;
        }
      })
      .catch((err) => {
        console.log(err);
      });

    //axios获取账户信息
    var accountoneurl = this.SERVICE_PATH + "account/one";
    var accountFormData = new FormData();
    accountFormData.append("account", this.account);
    this.axios
      .post(accountoneurl, accountFormData, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      })
      .then((res) => {
        //console.log(res.data.data)
        if (res.data.code == 200) {
          if (res.data.code == 200) {
            this.acccountInfo = res.data.data;
            this.acccountInfo.flag =
              this.acccountInfo.flag == 0
                ? "管理员"
                : this.acccountInfo.flag == 1
                ? "部长"
                : "普通";
            if (
              this.acccountInfo.avatar != null &&
              this.acccountInfo.avatar != ""
            ) {
              this.imgurl =
                "http://8.129.163.104/images/avatar/" +
                this.acccountInfo.avatar;
            } else {
              this.imgurl =
                "https://demos.creative-tim.com/vue-material-dashboard/img/marc.aba54d65.jpg";
            }
          }
        }
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>