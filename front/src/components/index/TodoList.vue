<template>
  <v-card class="ma-3 mb-auto">
    <v-list two-line>
      <v-list-item>
        <v-list-item-avatar tile size="100" rounded class="mt-n10">
          <v-sheet color="pink lighten-3" width="70" height="70" elevation="5" rounded>
            <v-icon dark large>fas fa-list-alt</v-icon>
          </v-sheet>
        </v-list-item-avatar>
        <v-list-item-content class="mt-n5 ml-2 font-weight-bold text-h4">
          <v-list-item-title>待 办 事 项</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-fab-transition>
        <v-btn
          v-show="!hidden"
          color="pink"
          @click="dialog = !dialog"
          dark
          absolute
          top
          right
          fab
          class="mr-5 mt-10"
        >
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-fab-transition>
      <v-text-field
        class="mx-4"
        color="blue"
        dense
        flat
        hide-details="auto"
        label="Search"
        outlined
        prepend-inner-icon="search"
      ></v-text-field>
      <v-list class="px-2 scrollable">
        <v-list-item-group v-model="selected" active-class="green--text">
          <template v-for="(item, index) in getItems">
            <v-list-item dense :key="item.id">
              <template v-slot:default="{ active, toggle }">
                <v-list-item-content>
                  <v-list-item-title class="font-weight-black" v-text="item.title">{{toggle}}</v-list-item-title>
                  <v-list-item-subtitle class="text--primary" v-text="item.subtitle"></v-list-item-subtitle>
                  <v-list-item-subtitle v-text="item.content"></v-list-item-subtitle>
                </v-list-item-content>

                <v-list-item-action>
                  <v-list-item-action-text v-text="item.action"></v-list-item-action-text>
                  <v-icon v-if="!active" color="grey lighten-1">star_border</v-icon>

                  <v-icon v-else color="yellow">star</v-icon>
                </v-list-item-action>
              </template>
            </v-list-item>

            <v-divider v-if="index + 1 < items.length" :key="index"></v-divider>
          </template>
        </v-list-item-group>
      </v-list>
    </v-list>
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="headline">待办事项</span>
        </v-card-title>
        <v-card-text class="pb-0">
          <v-container class="pb-0 mb-0">
            <v-form>
              <v-row>
                <v-col cols="12">
                  <v-text-field label="主标题" color="blue" v-model="todo.title"></v-text-field>
                  <v-text-field label="副标题" color="blue" v-model="todo.subtitle"></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-menu
                    ref="menuDate"
                    v-model="menuDate"
                    :close-on-content-click="false"
                    :return-value.sync="todo.deadlineDate"
                    transition="scale-transition"
                    offset-y
                    min-width="290px"
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-text-field
                        color="blue"
                        v-model="todo.deadlineDate"
                        label="截止日期"
                        prepend-inner-icon="event"
                        readonly
                        v-bind="attrs"
                        v-on="on"
                      ></v-text-field>
                    </template>
                    <v-date-picker v-model="todo.deadlineDate" no-title scrollable>
                      <v-spacer></v-spacer>
                      <v-btn text color="primary" @click="menuDate = false">取消</v-btn>
                      <v-btn text color="primary" @click="$refs.menuDate.save(todo.deadlineDate)">确认</v-btn>
                    </v-date-picker>
                  </v-menu>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-menu
                    ref="menu"
                    v-model="menu"
                    :close-on-content-click="false"
                    :nudge-right="40"
                    :return-value.sync="todo.deadlineTime"
                    transition="scale-transition"
                    offset-y
                    max-width="290px"
                    min-width="290px"
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-text-field
                        color="blue"
                        v-model="todo.deadlineTime"
                        label="截止时间"
                        prepend-inner-icon="access_time"
                        readonly
                        v-bind="attrs"
                        v-on="on"
                      ></v-text-field>
                    </template>
                    <v-time-picker
                      v-if="menu"
                      v-model="time"
                      full-width
                      @click:minute="$refs.menu.save(time)"
                    ></v-time-picker>
                  </v-menu>

                  <v-switch v-model="todo.state" inset label="紧急事项" class="mr-n16" color="red"></v-switch>
                </v-col>
                <v-col>
                  <v-textarea
                    color="blue"
                    label="内容"
                    outlined
                    rows="6"
                    row-height="25"
                    shaped
                    v-model="todo.content"
                  ></v-textarea>
                </v-col>
              </v-row>
            </v-form>
          </v-container>

          <small></small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false">关闭</v-btn>
          <v-btn color="blue darken-1" text @click="addTodo">添加</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-snackbar v-model="snackbar" :timeout="timeout">
      {{ text }}
      <template v-slot:action="{ attrs }">
        <v-btn color="blue" text v-bind="attrs" @click="snackbar = false">关闭</v-btn>
      </template>
    </v-snackbar>
    <!-- <v-container fluid class="fill-height">
          <v-row>
              <v-col cols="4" md="2">

              </v-col>
          </v-row>
    </v-container>-->
  </v-card>
</template>

<script>
export default {
  name: "TodoList",
  props: ["hidden"],
  computed: {
    getItems() {
      return this.items.map(
        (item, index) =>
          (item = {
            ...item,
            id: `t-${index}`
          })
      );
    }
  },
  data() {
    return {
      todo: {
        title: "",
        subtitle: "",
        content: "",
        deadlineDate: "",
        deadlineTime: "",
        state: false,
        checked: false
      },
      editedTodo: {
        title: "",
        subtitle: "",
        content: "",
        deadlineDate: "",
        deadlineTime: "",
        state: false,
        checked: false
      },
      checkbox: false,
      time: null,
      menuDate: false,
      modal: false,
      menu: false,
      selected: [],
      dialog: false,
      employee_id: localStorage.getItem("userid"),
      items: [],
      snackbar: false,
      timeout: 3000,
      text: ""
      // {
      //   action: "15 min",
      //   headline: "事项一",
      //   title: "完成报表",
      //   subtitle:
      //     "巴拉巴拉巴拉",
      // },
      // {
      //   action: "15 min",
      //   headline: "事项2",
      //   title: "约饭 ",
      //   subtitle:
      //     "巴拉巴拉巴拉",
      // },
    };
  },
  methods: {
    addTodo() {
      let form = new FormData();
      if (
        this.todo.title != "" &&
        this.todo.deadlineDate != "" &&
        this.todo.deadlineTime != ""
      ) {
        form.append("title", this.todo.title);
        form.append("subtitle", this.todo.subtitle);
        const deadline = `${this.todo.deadlineDate} ${this.todo.deadlineTime}:00`;
        form.append("deadline", deadline);
        form.append("content", this.todo.content);
        form.append("state", this.todo.state);
        this.axios
          .post(this.SERVICE_PATH + "addtodo", form, {
            params: { employee_id: this.employee_id },
            headers: { "Content-Type": "application/x-www-form-urlencoded" }
          })
          .then(res => {
            this.snackbar = true;
            if (res.data.code === 0) {
              this.text = "添加事项成功！~";
              this.dialog = false;
              this.items.push(this.todo);
            } else {
              this.text = "添加事项失败！~";
            }
          });
      } else {
        alert("请填写时间和标题！");
      }
    }
  },
  mounted() {
    this.axios
      .get(this.SERVICE_PATH + "gettodo", {
        params: {
          employee_id: this.employee_id
        }
      })
      .then(res => {
        this.items = res.data.data;
      });
  }
};
</script>

<style scoped>
.scrollable {
  height: 242px; /* or any height you want */
  overflow-y: auto;
}
</style>