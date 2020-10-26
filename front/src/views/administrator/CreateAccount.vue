<!--账户管理界面-->>
<template>
  <v-container id="create-account" fluid tag="section">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card style="margin-top:30px">
          <v-list-item two-line>
            <v-list-item-content>
              <v-list-item-title class="headline">创建账号</v-list-item-title>
              <v-list-item-subtitle>请输入员工信息</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-card-text>
            <v-form>
              <v-container class="py-0">
                <v-row>
                  <v-col cols="12" md="6">
                    <v-text-field v-model="employee.employee_id" label="工号" class="purple-input" clearable />
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-text-field v-model="employee.employee_name" label="姓名" class="purple-input" clearable />
                  </v-col>

                  <v-col cols="12" md="4">
                    <v-text-field v-model="employee.employee_title" label="职务" class="purple-input" clearable />
                  </v-col>

                  <v-col cols="12" md="4">
                    <v-text-field v-model="employee.department_name" label="所属部门" class="purple-input" clearable />
                  </v-col>

                  <v-col cols="12" md="4">
                    <v-text-field v-model="employee.leader_id" label="直属领导" class="purple-input" clearable />
                  </v-col>

                  <v-col cols="12" md="4">
                    <v-text-field v-model="employee.phone" label="联系电话" class="purple-input" type="phone" clearable />
                  </v-col>

                  <v-col cols="12" md="4">
                    <v-text-field v-model="employee.qq" label="QQ" class="purple-input" clearable />
                  </v-col>

                  <v-col cols="12" md="4">
                    <v-text-field v-model="employee.wechat" label="微信" class="purple-input" clearable />
                  </v-col>

                  <v-col cols="12" class="text-right">
                    <v-btn color="info" class="ma-2">
                      <vue-xlsx-table @on-select-file="leadingin">
                        <h3>导入EXCEL</h3>
                      </vue-xlsx-table>
                    </v-btn>
                    <v-snackbar v-model="leadinginsnackbar" left bottom :timeout="1500" color="primary" outlined>
                      工号为{{employee.employee_id}}的员工的信息导入成功
                      <template v-slot:action="{ snackbarattrs }">
                        <v-btn color="red" text v-bind="snackbarattrs" @click="leadinginsnackbar = false">
                          关闭
                        </v-btn>
                      </template>
                    </v-snackbar>
                    <v-btn color="info" class="ma-2" @click="resetting">
                      重置
                    </v-btn>
                    <v-dialog v-model="dialog" persistent max-width="290">
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn color="info" class="ma-2" dark v-bind="attrs" v-on="on">
                          创建
                        </v-btn>
                        <v-snackbar v-model="snackbar" left bottom :timeout="2000" color="primary" outlined>
                          {{newAccountResult}}
                          <template v-slot:action="{ snackbarattrs }">
                            <v-btn color="red" text v-bind="snackbarattrs" @click="snackbar = false">
                              关闭
                            </v-btn>
                          </template>
                        </v-snackbar>
                      </template>
                      <v-card>
                        <v-card-title class="headline">请核对信息</v-card-title>
                        <v-card-text>
                          <v-list-item>
                            <v-list-item-content>
                              <v-list-item-title>工号：{{employee.employee_id}}</v-list-item-title>
                            </v-list-item-content>
                          </v-list-item>
                          <v-list-item>
                            <v-list-item-content>
                              <v-list-item-title>姓名：{{employee.employee_name}}</v-list-item-title>
                            </v-list-item-content>
                          </v-list-item>
                          <v-list-item>
                            <v-list-item-content>
                              <v-list-item-title>职务：{{employee.employee_title}}</v-list-item-title>
                            </v-list-item-content>
                          </v-list-item>
                          <v-list-item>
                            <v-list-item-content>
                              <v-list-item-title>所属部门：{{employee.department_name}}</v-list-item-title>
                            </v-list-item-content>
                          </v-list-item>
                          <v-list-item>
                            <v-list-item-content>
                              <v-list-item-title>直属领导：{{employee.leader_id}}</v-list-item-title>
                            </v-list-item-content>
                          </v-list-item>
                          <v-list-item>
                            <v-list-item-content>
                              <v-list-item-title>联系电话：{{employee.phone}}</v-list-item-title>
                            </v-list-item-content>
                          </v-list-item>
                          <v-list-item>
                            <v-list-item-content>
                              <v-list-item-title>QQ：{{employee.qq}}</v-list-item-title>
                            </v-list-item-content>
                          </v-list-item>
                          <v-list-item>
                            <v-list-item-content>
                              <v-list-item-title>微信：{{employee.wechat}}</v-list-item-title>
                            </v-list-item-content>
                          </v-list-item>
                        </v-card-text>
                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn color="error darken-1" text @click="dialog = false">
                            <v-icon left>mdi-pencil</v-icon>修改
                          </v-btn>
                          <v-btn color="primary darken-1" text @click="newAccount">确认无误</v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                  </v-col>
                </v-row>
              </v-container>
            </v-form>
          </v-card-text>
        </v-card>

        <v-card style="margin-top:30px" height="300px">
          <v-card-title class="headline">新建账户信息显示</v-card-title>
          <v-card-subtitle>
            <v-radio-group v-model="acccountInfo.flag" row readonly>
              <v-radio label="管理员" value="0" color="red"></v-radio>
              <v-radio label="部长" value="1" color="info"></v-radio>
              <v-radio label="普通" value="2" color="success"></v-radio>
            </v-radio-group>
          </v-card-subtitle>
          <v-card-text class="text--primary">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field v-model="acccountInfo.account" label="账号" class="purple-input" readonly />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="acccountInfo.password" label="密码" class="purple-input" readonly />
              </v-col>
            </v-row>
          </v-card-text>
          <v-col cols="12" class="text-right">
            <v-snackbar v-model="leadingoutsnackbar" left bottom :timeout="2000" color="primary" outlined>
              正在导出工号为 {{acccountInfo.account}} 的员工的账户信息
              <template v-slot:action="{ snackbarattrs }">
                <v-btn color="red" text v-bind="snackbarattrs" @click="leadingoutsnackbar = false">
                  关闭
                </v-btn>
              </template>
            </v-snackbar>
            <!--<download-excel :data="oneaccount" :fields="accounts_json_fields" :before-generate="startDownload"
              :before-finish="finishDownload" :name="oneexcelname">
              <v-btn class="ma-2" color="info">
                导出ECXEL
              </v-btn>
            </download-excel>-->
            <v-btn class="ma-2" color="info" @click="export2ExcelOne">
              导出EXCEL
            </v-btn>
          </v-col>
        </v-card>
      </v-col>
    </v-row>

    <div id="load-wrapper">
      <v-card id="upload" class="py-2 px-4" color="rgba(0, 0, 0, .3)" dark flat link min-width="100"
        style="position: fixed; top: 200px; right: -35px; border-radius: 8px;">
        <v-icon large>
          mdi-cloud-upload
        </v-icon>
      </v-card>

      <v-card id="download" class="py-2 px-4" color="rgba(0, 0, 0, .3)" dark flat link min-width="100"
        style="position: fixed; top: 280px; right: -35px; border-radius: 8px;">
        <v-icon large>
          mdi-cloud-download
        </v-icon>
      </v-card>

      <v-menu v-model="unloadmenu" :close-on-content-click="false" activator="#upload" bottom content-class="v-settings"
        left nudge-left="8" offset-x origin="top right" transition="scale-transition" @click="uploadExpand">
        <v-card class="text-center mb-0" width="200">
          <v-card-text>
            <strong class="mb-3 d-inline-block">一键导入员工基本信息</strong>
            <vue-xlsx-table @on-select-file="handleSelectedFile">
              <h4>一键导入EXCEL</h4>
            </vue-xlsx-table>
          </v-card-text>
        </v-card>
      </v-menu>
      <v-snackbar v-model="uploadsnackbar" left bottom :timeout="2000" color="primary" outlined>
        员工基本信息导入成功
        <template v-slot:action="{ snackbarattrs }">
          <v-btn color="red" text v-bind="snackbarattrs" @click="uploadsnackbar = false">
            关闭
          </v-btn>
        </template>
      </v-snackbar>

      <v-menu v-model="downloadmenu" :close-on-content-click="false" activator="#download" bottom
        content-class="v-settings" left nudge-left="8" offset-x origin="top right" transition="scale-transition"
        @click="downloadExpand">
        <v-card class="text-center mb-0" width="200">
          <v-card-text>
            <strong class="mb-3 d-inline-block">一键导出所有员工账户信息</strong>
            <!--采用vue-josn-excel导出，导出的文件格式和扩展名不匹配-->
            <!--<download-excel :data="accounts_json_data" :fields="accounts_json_fields" title="员工账户信息一览表"
              worksheet="accounts" name="所有账户信息.xls">
              <v-btn small class="mb-3" color="success" @click="downloadaccounts">
                一键导出EXCEL
              </v-btn>
            </download-excel>-->

            <!--采用file-saver xlsx script-loader导出ecxel-->
            <v-btn small class="mb-3" color="success" @click="export2ExcelAll">
              一键导出EXCEL
            </v-btn>
          </v-card-text>
        </v-card>
      </v-menu>
      <v-snackbar v-model="downloadsnackbar" left bottom :timeout="2000" color="primary" outlined>
        正在导出所有员工账户信息
        <template v-slot:action="{ snackbarattrs }">
          <v-btn color="red" text v-bind="snackbarattrs" @click="downloadsnackbar = false">
            关闭
          </v-btn>
        </template>
      </v-snackbar>
    </div>
  </v-container>
</template>

<script>
  export default {
    // 注入依赖
    inject: ['reload'],
    name: 'CreateAccount',
    components: {

    },
    data() {
      return {
        employee: {
          employee_id: "",
          employee_name: "",
          employee_title: "",
          department_name: "",
          leader_id: "",
          phone: "",
          qq: "",
          wechat: ""
        },
        oneexcelname: "",
        unloadmenu: false,
        downloadmenu: false,

        leadinginsnackbar: false,
        leadingoutsnackbar: false,
        uploadsnackbar: false,
        downloadsnackbar: false,
        snackbar: false,
        dialog: false,

        department_name: "",
        department_names: [],
        department_ids: [],

        acccountInfo: {
          user_id: "",
          account: "",
          password: "",
          flag: null
        },
        oneaccount: [],
        accounts_json_data: [],
        
        /*
        accounts_json_fields: {
          "序号": "user_id",
          "账号": "account",
          "密码": "password",
          "账户类型": {
            field: 'flag',
            callback: (value) => {
              if (value) {
                return value == 1 ? "部长" : "普通"
              } else {
                return '管理员'
              }
            }
          }
        },*/

        // 新增员工的返回结果
        newAccountResult: "",

        excel2json: {
          department_names: [],
          employees: []
        },
        employeeInfo: {
          employee_id: "",
          employee_name: "",
          employee_title: "",
          department_name: "",
          leader_id: "",
          phone: "",
          qq: "",
          wechat: ""
        }
      }
    },
    methods: {
      //一键导入excel
      handleSelectedFile(convertedData) {
        //console.log(convertedData.header) 表头信息
        convertedData.body.forEach(element => {
          //console.log(element)
          //统计部门名称
          if (this.excel2json.department_names.indexOf(element.所属部门) == -1) {
            this.excel2json.department_names.push(element.所属部门)
          }
          // 保存员工信息
          this.employeeInfo.employee_id = element.工号
          this.employeeInfo.employee_name = element.姓名
          this.employeeInfo.employee_title = element.职务
          this.employeeInfo.department_name = typeof (element.所属部门) == "undefined" ? null : element.所属部门
          this.employeeInfo.leader_id = typeof (element.直属领导) == "undefined" ? null : element.直属领导
          this.employeeInfo.phone = typeof (element.联系电话) == "undefined" ? null : element.联系电话
          this.employeeInfo.qq = typeof (element.QQ) == "undefined" ? null : element.QQ
          this.employeeInfo.wechat = typeof (element.微信) == "undefined" ? null : element.微信
          this.excel2json.employees.push(this.employeeInfo)
          // 清空
          this.employeeInfo = {
            employee_id: "",
            employee_name: "",
            employee_title: "",
            department_name: "",
            leader_id: "",
            phone: "",
            qq: "",
            wechat: ""
          }
        });
        //console.log(this.excel2json)
        //将员工基本信息的json数据传输到后台
        var inurl = this.SERVICE_PATH + 'employee/add'
        this.axios.post(inurl, this.excel2json, {
            headers: {
              'Content-Type': 'application/json'
            }
          })
          .then(res => {
            //console.log(res.data)
            if (res.data.code == 200) {
              this.uploadsnackbar = true
            }
          })
          .catch((err) => {
            console.log(err)
          })
      },


      formatJson(filterVal, jsonData) {
        return jsonData.map(v => filterVal.map(j => v[j]))
      },
      export2Excel(rawdata, excelname) {
        require.ensure([], () => {
          const {
            export_json_to_excel
          } = require('@/excel/Export2Excel');
          const tHeader = ['序号', '账号', '密码', '账户类型']; // 设置Excel表格的表头
          const filterVal = ['user_id', 'account', 'password', 'flag']; // 表头对应的数据
          const list = rawdata; // 把数据存到list
          const data = this.formatJson(filterVal, list);
          export_json_to_excel(tHeader, data, excelname); // 设置Excel表格的文件名
        })
      },
      export2ExcelOne() {
        if (this.acccountInfo.account != "") {
          var excelname = "工号为" + this.acccountInfo.account + "的员工账户信息"
          this.export2Excel(this.oneaccount, excelname)
          this.leadingoutsnackbar = true
        }

      },
      export2ExcelAll() {
        this.export2Excel(this.accounts_json_data, '所有员工的账户信息')
        this.downloadsnackbar = true
      },


      /*downloadaccounts() {
        this.downloadsnackbar = true
      },
      startDownload() {
        if (this.acccountInfo.account != "") {
          this.oneexcelname = "工号为" + this.acccountInfo.account + "的员工账户信息.xls"
          this.leadingoutsnackbar = true
        }
      },
      finishDownload() {
        this.clear()
      },*/

      uploadExpand() {
        this.unloadmenu = true,
          this.downloadmenu = false
      },
      downloadExpand() {
        this.unloadmenu = false,
          this.downloadmenu = true
      },

      leadingin(convertedData) {
        //导入单个员工信息
        var element = convertedData.body[0]
        this.employee.employee_id = element.工号
        this.employee.employee_name = element.姓名
        this.employee.employee_title = element.职务
        this.employee.department_name = typeof (element.所属部门) == "undefined" ? "" : element.所属部门
        this.employee.leader_id = typeof (element.直属领导) == "undefined" ? "" : element.直属领导
        this.employee.phone = typeof (element.联系电话) == "undefined" ? "" : element.联系电话
        this.employee.qq = typeof (element.QQ) == "undefined" ? "" : element.QQ
        this.employee.wechat = typeof (element.微信) == "undefined" ? "" : element.微信
        this.leadinginsnackbar = true
      },
      clear() {
        //清除
        this.acccountInfo = {
          user_id: "",
          account: "",
          password: "",
          flag: null
        }
        this.oneaccount = []
      },

      resetting() {
        // 重置员工信息
        this.employee = {
          employee_id: "",
          employee_name: "",
          employee_title: "",
          department_name: "",
          leader_id: "",
          phone: "",
          qq: "",
          wechat: ""
        }

      },
      newAccount() {
        // 工号、姓名、职务不能为空
        if (this.employee.employee_id != "" && this.employee.employee_name != "" && this.employee.employee_title !=
          "") {
          // 关闭对话框
          this.dialog = false
          // 记录新员工工号
          let id = this.employee.employee_id
          // 向后台传输数据
          let newaccounturl = this.SERVICE_PATH + 'employee/addone'
          let employeeFormData = new FormData()
          employeeFormData.append('employee_id', this.employee.employee_id)
          employeeFormData.append('employee_name', this.employee.employee_name)
          employeeFormData.append('employee_title', this.employee.employee_title)
          employeeFormData.append('department_name', this.employee.department_name)
          employeeFormData.append('leader_id', this.employee.leader_id)
          employeeFormData.append('phone', this.employee.phone)
          employeeFormData.append('qq', this.employee.qq)
          employeeFormData.append('wechat', this.employee.wechat)
          this.axios.post(newaccounturl, employeeFormData, {
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
              }
            })
            .then(res => {
              //console.log(res.data)
              if (res.data.code == 200) {
                this.acccountInfo.user_id = res.data.data.user_id
                this.acccountInfo.account = res.data.data.account
                this.acccountInfo.password = res.data.data.password
                this.acccountInfo.flag = res.data.data.flag + ""
                this.oneaccount.push(this.acccountInfo)
                this.newAccountResult = '工号为' + id + '员工账号创建成功'
                this.snackbar = true
              } else if (res.data.code == 201) {
                this.newAccountResult = '工号为' + id + '员工账号创建失败'
                this.snackbar = true
              } else if (res.data.code == 202) {
                this.newAccountResult = res.data.data
                this.snackbar = true
              } else {
                console.log()
              }
            })
            .catch((err) => {
              console.log(err)
            })
        }else{
          alert("工号、姓名、职务都不能为空")
        }
      }
    },
    mounted() {
      /**axios 获取 department.json
       * var allDepartmentUrl = './department.json'
       */
      //通过后台接口获取数据
      var allDepartmentUrl = this.SERVICE_PATH + "department/all"
      this.axios.get(allDepartmentUrl)
        .then(res => {
          //console.log(res.data)
          if (res.data.code == 200) {
            for (var i = 0; i < res.data.length; i++) {
              this.department_names.push(res.data[i].department_name)
              this.department_ids.push(res.data[i].department_id)
            }
          }
        })
        .catch((err) => {
          console.log(err)
        })

      // axios 获取员工账户信息(过滤第一条)按account升序
      var accountallurl = this.SERVICE_PATH + "account/all"
      this.axios.get(accountallurl)
        .then(res => {
          //console.log(res.data)
          if (res.data.code == 200) {
            this.accounts_json_data = res.data.data
            this.accounts_json_data.forEach(element => {
              if (element.flag == 0) {
                element.flag = "管理员"
              }
              if (element.flag == 1) {
                element.flag = "部长"
              }
              if (element.flag == 2) {
                element.flag = "普通"
              }
            });
          }
        })
        .catch((err) => {
          console.log(err)
        })
    }
  }
</script>