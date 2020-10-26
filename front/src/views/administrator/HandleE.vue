<template>
  <v-container id="employees-table" fluid tag="section">
    <v-row>
      <v-col v-for="(item, i) in employee_counts_in_department" :key="i" cols="12" sm="6" lg="3">
        <v-card class="mx-auto" max-width="400">
          <v-img class="white--text align-end" height="200px" src="../../assets/bg_login.png">
            <v-card-title>{{item.department_name}}</v-card-title>
          </v-img>
          <v-card-subtitle class="pb-0">总人数：{{item.department_employees}}
          </v-card-subtitle>
          <v-card-text class="text--primary">
            <div>话事人姓名：{{item.department_minister?item.department_minister.minister_name:'None'}}</div>
            <div>话事人工号：{{item.department_minister?item.department_minister.minister_id:'None'}}</div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12">
        <v-card>
          <v-card-title>
            员工信息一览表
            <v-divider class="mx-4" inset vertical />
            <v-spacer></v-spacer>
            <v-text-field v-model="search" append-icon="mdi-magnify" label="请输入关键词" single-line hide-details>
            </v-text-field>
          </v-card-title>
          <v-data-table class="elevation-1" :headers="headers" :items="employeesInfo" :search="search"
            :expanded.sync="expanded" item-key="employee_id" show-expand no-results-text="匹配数据为空" no-data-text="表格为空"
            :footer-props="{showFirstLastPage: true,firstIcon: 'mdi-arrow-collapse-left',lastIcon: 'mdi-arrow-collapse-right',prevIcon: 'mdi-menu-left',nextIcon: 'mdi-menu-right',
            itemsPerPageText:'每页个数',itemsPerPageOptions: [5, 10, 20, 50, 100]}">
            <!--修改pageText  原始:1-10 of 11   修改后：第1 - 10条，共11条-->
            <template v-slot:footer.page-text="items"> 第{{ items.pageStart }} - {{ items.pageStop }}条，共
              {{ items.itemsLength }}条 </template>

            <!--编辑对话框-->
            <template v-slot:top>
              <v-dialog v-model="dialog" max-width="500px">
                <v-card>
                  <v-card-title>
                    <span class="headline">更新员工信息</span>
                  </v-card-title>
                  <v-card-text>
                    <v-container>
                      <v-row>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field v-model="editedItem.employee_id" label="工号"></v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field v-model="editedItem.employee_name" label="姓名"></v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field v-model="editedItem.employee_title" label="职务"></v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field v-model="editedItem.department_id" label="所属部门"></v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field v-model="editedItem.leader_id" label="直属领导"></v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field v-model="editedItem.phone" label="联系电话"></v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field v-model="editedItem.qq" label="QQ"></v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field v-model="editedItem.wechat" label="微信"></v-text-field>
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
            </template>

            <!--扩展数据填充-->
            <template v-slot:expanded-item="{ headers,item}">
              <td :colspan="headers.length" color="primary">
                {{accountsInfo[employeesInfo.indexOf(item)]}}
              </td>
            </template>
            <!--操作按钮填充-->
            <template v-slot:item.actions="{item}">
              <v-icon small color="primary" class="mr-2" @click="editItem(item)">mdi-pencil</v-icon>
              <v-icon small color="red" @click="deleteItem(item)">mdi-delete</v-icon>
            </template>
            <!--姓名颜色填充-->
            <template v-slot:item.employee_name="{item}">
              <v-chip :color="getColor(item.employee_title)" dark>{{ item.employee_name }}</v-chip>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

  </v-container>
</template>

<script>
  export default {
    // 注入依赖
    inject: ['reload'],
    data() {
      return {
        //是否打开对话框
        dialog: false,

        // 扩展信息数组
        expanded: [],

        //是否单个展开
        singleExpand: false,

        editedIndex: -1,
        editedItem: {
          employee_id: "",
          employee_name: "",
          employee_title: "",
          department_name: "",
          leader_id: "",
          phone: "",
          qq: "",
          wechat: ""
        },
        defaultItem: {
          employee_id: "",
          employee_name: "",
          employee_title: "",
          department_name: "",
          leader_id: "",
          phone: "",
          qq: "",
          wechat: ""
        },

        //查询关键词
        search: '',

        //表头
        headers: [{
            text: '工号',
            align: 'start',
            value: 'employee_id',
          },
          {
            text: '姓名',
            value: 'employee_name'
          },
          {
            text: '职务',
            value: 'employee_title'
          },
          {
            text: '所属部门',
            value: 'department_id'
          },
          {
            text: '直属领导',
            value: 'leader_id'
          },
          {
            text: '联系电话',
            value: 'phone'
          },
          {
            text: 'QQ',
            value: 'qq'
          },
          {
            text: '微信',
            value: 'wechat'
          },
          {
            text: '账户信息',
            value: 'data-table-expand'
          },
          {
            text: '操作',
            value: 'actions',
            sortable: false
          },
        ],
        //表格数据
        employeesInfo: [],

        //扩展数据
        accountsInfo: [],

        //各部门员工总数
        employee_counts_in_department: [],

        //部门名称信息
        department_names: [],
        //部门编号信息
        department_ids: [],
      }
    },
    watch: {
      dialog(val) {
        val || this.close()
      },
    },
    methods: {
      editItem(item) {
        this.editedIndex = this.employeesInfo.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },
      deleteItem(item) {
        const index = this.employeesInfo.indexOf(item)
        // 记录该员工id
        let id = item.employee_id
        var str = item.employee_id + ":" + item.employee_name
        let deleteidFormData = new FormData()
        deleteidFormData.append('employee_id', id)
        var result = confirm('确认要删除员工 ' + str + ' 吗?')
        if (result == true) {
          //将该员工的 employee_id 传向后台
          var deleteurl = this.SERVICE_PATH + 'employee/delete'
          this.axios.post(deleteurl, deleteidFormData, {
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
              }
            })
            .then(res => {
              //console.log(res.data.data)
              if (res.data.code == 200) {
                alert("员工" + id + "删除成功")
                //刷新页面
                this.reload()
              } else if (res.data.code == 201) {
                alert("员工" + id + "删除失败")
              } else if (res.data.code == 203) {
                alert(res.data.data)
              } else {
                console.log()
              }
            })
            .catch((err) => {
              console.log(err)
            })

          //在表格中删除该员工
          this.employeesInfo.splice(index, 1)
        }
      },
      close() {
        this.dialog = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },
      save() {
        if (this.editedIndex > -1) {
          //将该员工的信息传向后台，在数据库中更新
          var updateurl = this.SERVICE_PATH + 'employee/update'
          let id = this.editedItem.employee_id
          let employeeFormData = new FormData()
          employeeFormData.append('employee_id', this.editedItem.employee_id)
          employeeFormData.append('employee_name', this.editedItem.employee_name)
          employeeFormData.append('employee_title', this.editedItem.employee_title)
          employeeFormData.append('department_name', this.editedItem.department_id)
          employeeFormData.append('leader_id', this.editedItem.leader_id)
          employeeFormData.append('phone', this.editedItem.phone)
          employeeFormData.append('qq', this.editedItem.qq)
          employeeFormData.append('wechat', this.editedItem.wechat)
          this.axios.post(updateurl, employeeFormData, {
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
              }
            })
            .then(res => {
              //console.log(res.data)
              if (res.data.code == 200) {
                alert('员工' + id + '的基本信息更新成功')
                //刷新页面
                this.reload()
              } else if (res.data.code == 201) {
                alert('员工' + id + '的基本信息更新失败')
              } else if (res.data.code == 202) {
                alert(res.data.data)
              } else {
                console.log()
              }
            })
            .catch((err) => {
              console.log(err)
            })

          //在表格中更新员工信息
          Object.assign(this.employeesInfo[this.editedIndex], this.editedItem)
        } else {
          this.employeesInfo.push(this.editedItem)
        }
        this.close()
      },
      getColor(employee_title) {
        if (employee_title == "") return 'red'
        else if (employee_title == "部长") return 'info'
        else return 'success'
      }
    },
    mounted() {
      //axios 获取部门信息 按department_id升序
      var allDepartmentUrl = this.SERVICE_PATH + "department/all"
      this.axios.get(allDepartmentUrl)
        .then(res => {
          //console.log(res.data.data)
          if (res.data.code == 200) {
            this.department_nums = res.data.data.length
            for (var i = 0; i < res.data.data.length; i++) {
              //部门名称数组
              this.department_names.push(res.data.data[i].department_name)
              //部门编号数组
              this.department_ids.push(res.data.data[i].department_id)
            }
          }
        })
        .catch((err) => {
          console.log(err)
        })

      // axios 获取员工基本信息 按employee_id升序
      var employeeallurl = this.SERVICE_PATH + "employee/all"
      this.axios.get(employeeallurl)
        .then(res => {
          //console.log(res.data.data)
          if (res.data.code == 200) {
            this.employeesInfo = res.data.data
            for (var i = 0; i < this.employeesInfo.length; i++) {
              // 将 department_id 转换为 department_name 显示
              var id = this.employeesInfo[i].department_id
              this.employeesInfo[i].department_id = this.department_names[this.department_ids.indexOf(id)]
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
            res.data.data.forEach(element => {
              var type = ""
              if (element.flag == 0) {
                type = "管理员"
              }
              if (element.flag == 1) {
                type = "部长"
              }
              if (element.flag == 2) {
                type = "普通"
              }
              this.accountsInfo.push("账号：" + element.account + "密码：" + element.password + "账号类型：" + type)
            });
          }
        })
        .catch((err) => {
          console.log(err)
        })

      // axios 获取各部门员工数目
      var employeecountsindepartmenturl = this.SERVICE_PATH + "employee/d_nums"
      this.axios.get(employeecountsindepartmenturl)
        .then(res => {
          //console.log(res.data)
          if (res.data.code == 200) {
            res.data.data.forEach(element => {
              this.employee_counts_in_department.push(element)
            });
          }
        })
        .catch((err) => {
          console.log(err)
        })
    }
  }
</script>