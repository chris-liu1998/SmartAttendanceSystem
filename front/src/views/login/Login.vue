<template>
  <v-app>
    <div class="background">
      <v-container fluid class="fill-height">
        <v-row justify="center" align="center">
          <v-col cols="12" sm="auto" md="auto">
            <div class="login">
              <div class="left">
                <v-card height="433" width="433" color="#556bbf">
                  <div class="left-text">
                    <div class="text-h4 white--text" font="Robot">欢迎使用</div>
                    <div class="text-h6 white--text" font="Robot">智慧考勤系统</div>
                  </div>
                  <v-img class="computers" src="@/assets/computers.png" width="400"></v-img>
                </v-card>
              </div>
              <div class="right">
                <v-card height="433" width="300">
                  <v-card-text>
                    <div
                      class="text-h6 text-center font-weight-bold accent--text mb-5"
                      font="Robot"
                    >登录</div>
                    <v-form>
                      <v-text-field
                        label="请输入账号"
                        v-model="account"
                        prepend-icon="mdi-account"
                        autocomplete
                      ></v-text-field>
                      <v-text-field
                        v-model="password"
                        label="请输入密码"
                        prepend-icon="mdi-lock"
                        type="password"
                        autocomplete
                      ></v-text-field>
                      <v-row>
                        <v-col>
                          <v-text-field v-model="verifycode" label="请输入验证码"></v-text-field>
                        </v-col>
                        <v-col>
                          <v-img
                            class="captcha-img"
                            id="verify_code"
                            width="100"
                            height="35"
                            @click="changeCaptcha"
                            :src="imgurl"
                          />
                        </v-col>
                      </v-row>
                    </v-form>
                  </v-card-text>
                  <v-card-actions class="pt-0">
                    <v-row>
                      <v-col>
                        <v-btn class="mb-3" color="#556bbf" block dark @click="login">登录</v-btn>
                        <v-btn text block @click="forget_password">忘记密码</v-btn>
                      </v-col>
                    </v-row>
                  </v-card-actions>
                </v-card>
              </div>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </v-app>
</template>

<style scoped>
body,
html {
  margin: 0;
  width: 100%;
  height: 100%;
}
.background {
  background: url("../../assets/bg_login.png");

  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  width: 100%;
  height: 100%;
}

.left-text {
  position: absolute;
  top: 8%;
  left: 8%;
}

.computers {
  position: absolute;
  top: 40%;
  left: 4%;
}

.left {
  float: left;
}

.right {
  float: left;
}
</style>


<script>
export default {
  // 注入依赖
  inject: ["reload"],
  data: () => ({
    account: "",
    password: "",
    verifycode: "",
    imgurl: "",
  }),

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      //this.imgurl = this.SERVICE_PATH + "captchaimg";
      this.imgurl = this.SERVICE_PATH + "captchaimg?" + Math.random();
    },

    changeCaptcha() {
      this.imgurl = this.SERVICE_PATH + "captchaimg?" + Math.random();
    },

    login() {
      var that = this;
      if (this.account.length == 0) {
        alert("账户不能为空！");
      } else if (this.password.length == 0) {
        alert("密码不能为空！");
      } else if (this.verifycode.length == 0) {
        alert("验证码不能为空！");
      } else {
        var params = new URLSearchParams();
        params.append("account", this.account);
        params.append("password", this.password);
        params.append("captcha", this.verifycode);

        this.axios
          .post(this.SERVICE_PATH + "login", params, { withCredentials: true })
          .then(function (res) {
            if (res.data.code == 201) {
              alert("验证码错误！");
              that.imgurl = that.SERVICE_PATH + "captchaimg?" + Math.random();
            }
            if (res.data.code == 202) {
              alert("密码错误！");
              that.imgurl = that.SERVICE_PATH + "captchaimg?" + Math.random();
            }
            if (res.data.code == 203) {
              alert("账户不存在！");
              that.imgurl = that.SERVICE_PATH + "captchaimg?" + Math.random();
            }
            if (res.data.code == 200) {
              if (that.account == "Admin") {
                that.$store.commit("login", {
                  userid: res.data.data.userid,
                  flag: res.data.data.flag,
                  departmentid: 0,
                });
              } else {
                that.$store.commit("login", {
                  userid: res.data.data.userid,
                  flag: res.data.data.flag,
                  departmentid: res.data.data.departmentid,
                });
              }
              var path = that.$route.query.redirect;
              that.$router.replace({
                path: path === "/" || path === undefined ? "/" : path,
              });
            }
          })
          .catch(function (error) {
            console.log(error);
          });
      }
    },

    forget_password() {
      alert("请联系系统管理员或上级！");
    },
  },
};
</script>