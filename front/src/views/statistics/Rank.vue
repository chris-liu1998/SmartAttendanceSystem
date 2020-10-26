<template>
  <v-container fluid>
    <!-- <v-breadcrumbs :items="breadcrumbs" divider=">"></v-breadcrumbs> -->
    <v-row>
      <v-col cols="auto" md="9">
        <v-row>
          <v-spacer></v-spacer>
          <v-btn class="mr-5 mb-3" outlined color="indigo" @click="export2ExcelAll">导出表格</v-btn>
        </v-row>

        <RankTable :headers="headers" :items="sortedItemsWithRank" :loading="loading" class="mx-2" />
      </v-col>
      <v-col cols="auto" md="3">
        <div class="d-flex flex-column">
          <v-select
            v-model="selection"
            :items="items"
            item-text="desc"
            item-value="value"
            label="排序指标"
            return-object
            dense
          ></v-select>
          <v-date-picker elevation="3" v-model="dates" range class="mx-auto mb-5"></v-date-picker>
          <v-text-field
            class="text-field"
            
            v-model="dateRangeText"
            label="日期范围"
            prepend-inner-icon="event"
            readonly
          ></v-text-field>
          <v-btn class="ma-2" outlined color="indigo" @click="rankByDateRange">查询</v-btn>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import RankTable from "@/components/admin/RankTable";
export default {
  name: "Rank",
  components: {
    RankTable,
  },
  computed: {
    sortedItemsWithRank() {
      return this.sortByAttr(); //排序
    },
    dateRangeText() {
      return this.dates.join(" ~ ");
    },
  },
  methods: {
    formatJson(filterVal, jsonData) {
      return jsonData.map((v) => filterVal.map((j) => v[j]));
    },
    export2ExcelAll() {
      this.export2Excel(this.sortedItemsWithRank, "员工的考勤排行信息");
      this.downloadsnackbar = true;
    },
    export2Excel(rawdata, excelname) {
      require.ensure([], () => {
        const { export_json_to_excel } = require("@/excel/Export2Excel");
        const tHeader = [
          "工号",
          "姓名",
          "部门",
          "职务",
          "请假",
          "缺勤",
          "迟到",
          "早退",
          "出勤率（%）",
        ]; // 设置Excel表格的表头
        const filterVal = [
          "employee_id",
          "name",
          "dep",
          "role",
          "leave",
          "absence",
          "late",
          "leave_early",
          "attend_rate",
        ]; // 表头对应的数据
        const list = rawdata; // 把数据存到list
        const data = this.formatJson(filterVal, list);
        export_json_to_excel(tHeader, data, excelname); // 设置Excel表格的文件名
      });
    },
    compareDate(dates) {
      let date_one = new Date(dates[0]);
      let date_two = new Date(dates[1]);
      if (date_one > date_two) {
        let temp = dates[0];
        dates[0] = dates[1];
        dates[1] = temp;
      }
      return dates;
    },
    sortByAttr() {
      switch (this.selection.value) {
        case "1":
          return this.employees.sort((a, b) => b.attend_rate - a.attend_rate);
        case "2":
          return this.employees.sort((a, b) => b.leave - a.leave);
        case "3":
          return this.employees.sort((a, b) => b.absence - a.absence);
        case "4":
          return this.employees.sort((a, b) => b.late - a.late);
        case "5":
          return this.employees.sort((a, b) => b.leave_early - a.leave_early);
        default:
          break;
      }
    },
    initialize() {
      this.loading = true;
      this.axios.get(this.SERVICE_PATH + "rank").then((res) => {
        this.employees = res.data.data;
        this.loading = false;
      });
    },
    rankByDateRange() {
      this.loading = true;
      let dates = this.dates;
      let end_date = null;
      if (this.dates.length === 2) {
        dates = this.compareDate(dates);
        end_date = dates[1];
      }

      let start_date = dates[0];

      this.axios
        .get(this.SERVICE_PATH + "rank", {
          params: {
            start_date: start_date,
            end_date: end_date,
          },
        })
        .then((res) => {
          this.employees = res.data.data;
          this.loading = false;
        });
    },
  },
  mounted() {
    this.initialize();
    //console.log(this.$vuetify.breakpoint.name);
  },
  data: () => ({
    loading: true,
    dates: [],
    selection: { desc: "按考勤率排名", value: "1" },
    items: [
      { desc: "按考勤率排名", value: "1" },
      { desc: "按请假次数排名", value: "2" },
      { desc: "按缺勤次数排名", value: "3" },
      { desc: "按迟到次数排名", value: "4" },
      { desc: "按早退次数排名", value: "5" },
    ],
    headers: [
      {
        text: "排名",
        align: "start",
        sortable: false,
        value: "rank",
      },
      { text: "工号", value: "employee_id", sortable: false },
      { text: "姓名", value: "name", sortable: false },
      { text: "部门", value: "dep", sortable: false },
      { text: "职务", value: "role", sortable: false },
      { text: "请假", value: "leave", sortable: false },
      { text: "缺勤", value: "absence", sortable: false },
      { text: "迟到", value: "late", sortable: false },
      { text: "早退", value: "leave_early", sortable: false },
      { text: "出勤率(%)", value: "attend_rate", sortable: false },
      { text: "详情", value: "action", sortable: false },
    ],
    employees: [],
  }),
};
</script>
<style scoped>
/* .text-field {
  width: 200px;
} */
</style>