<template>
  <v-card>
    <v-card-title>
      排名
      <v-spacer></v-spacer>
      <v-text-field v-model="search" append-icon="mdi-magnify" label="搜索"></v-text-field>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="employeesWithRanks"
      :item-key="employeesWithRanks.work_num"
      :search="search"
      :loading="loading"
      loading-text="加载中……"
      :footer-props="{
      showFirstLastPage: true,
      firstIcon: 'mdi-arrow-collapse-left',
      lastIcon: 'mdi-arrow-collapse-right',
      prevIcon: 'mdi-minus',
      nextIcon: 'mdi-plus'
    }"
    >
      <template v-slot:item.name="{ item }">
        <!--这里Eslint报错无所谓-->
        <v-chip :color="getColor(item.rank)" dark>{{ item.name }}</v-chip>
      </template>
      <template v-slot:item.attend_rate="{ item }">
        <!--这里Eslint报错无所谓-->
        <v-progress-linear rounded striped height="15" v-model="item.attend_rate">
          <strong class="text-caption">{{item.attend_rate}}%</strong>
        </v-progress-linear>
      </template>
      <template v-slot:item.action="{ item }">
        <!--这里Eslint报错无所谓-->
        <v-icon small @click="getDetails(item)">description</v-icon>
      </template>
    </v-data-table>

    <v-dialog v-model="dialog" width="800">
      <v-card>
        <v-card-title class="headline grey lighten-2">
          <b>{{employee_name}}</b> 的打卡详情
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-spacer></v-spacer>
            <v-btn color="info" text @click="dialog = false">确定</v-btn>
          </v-card-actions>
        </v-card-title>

        <RankDetail :employee="employee_id" class="mx-2"></RankDetail>

        <v-divider></v-divider>
      </v-card>
    </v-dialog>
  </v-card>
</template>
<script>
import RankDetail from "@/components/admin/RankDetail.vue";
export default {
  components: {
    RankDetail
  },
  name: "RankTable",
  computed: {
    employeesWithRanks() {
      let result = this.items.map((item, i) => {
        if (!item.rank) {
          item = {
            ...item,
            rank: i + 1
          };
        } else {
          item.rank = i + 1;
        }
        return item;
      });

      return result;
    }
  },
  props: ["headers", "items", "loading"],
  data() {
    return {
      dialog: false,
      search: "",
      employee_id: "",
      employee_name: ""
    };
  },
  methods: {
    getColor(rank) {
      switch (rank) {
        case 1:
          return "red";
        case 2:
          return "orange";
        case 3:
          return "yellow";
        default:
          return "green";
      }
    },
    getDetails(employees) {
      this.dialog = true;

      this.employee_id = employees.employee_id;
      this.employee_name = employees.name;
      return employees;
    },
    close() {
      this.employee_id = "";
      dialog = false;
    }
  }
};
</script>