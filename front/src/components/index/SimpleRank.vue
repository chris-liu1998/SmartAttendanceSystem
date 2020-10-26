
<template>
  <v-card class="ma-3 mb-auto" tile>
    <v-list-item>
      <v-list-item-avatar tile size="100" rounded class="mt-n8">
        <v-sheet color="orange darken-1" width="70" height="70" elevation="5" rounded>
          <v-icon dark large>fas fa-list-ol</v-icon>
        </v-sheet>
      </v-list-item-avatar>
      <v-list-item-content class="font-weight-bold">昨日排行</v-list-item-content>
    </v-list-item>
    <v-list-item v-for="(item, id) in items" :key="id">
      <v-list-item-content>
        <v-list-item-title v-text="id+1" align="center"></v-list-item-title>
      </v-list-item-content>
      <v-list-item-content>
        <v-list-item-title v-text="item.姓名" align="center"></v-list-item-title>
      </v-list-item-content>
      <v-list-item-content>
        <v-list-item-title v-text="item.出勤率" align="center"></v-list-item-title>
      </v-list-item-content>
    </v-list-item>
  </v-card>
</template>


<script>
export default {
  name: "SimpleRank",
  data: () => ({
    items: [],
  }),
  mounted() {
    this.axios.get(this.SERVICE_PATH + "simplerank").then((res) => {
      this.items = res.data.data;
    });
  },
};
</script>

<style>
.center1 {
  margin: 0 auto;
  width: 70%;
}
</style>