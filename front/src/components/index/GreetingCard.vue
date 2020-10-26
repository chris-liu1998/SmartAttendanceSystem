<template>
  <v-card class="ma-3" height="180">
    <v-list-item>
      <v-list-item-avatar tile size="100" rounded class="mt-n16">
        <v-sheet color="green" width="70" height="70" elevation="5" rounded>
          <v-icon dark large>far fa-smile-wink</v-icon>
        </v-sheet>
      </v-list-item-avatar>
      <v-list-item-content class="ml-12">
        <v-list-item-title
          class="my-3 text-h4 font-weight-black grey--text text--darken-3"
        >{{hours}}好，{{name}} ;）</v-list-item-title>
        <v-list-item-subtitle
          class="text-h6 text--disabled font-weight-bold"
        >今天是{{month}}月{{date}}日，星期{{day}}</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title class="text-center font-weight-medium text-h6">“{{saying}}”</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
  </v-card>
</template>
<script>
export default {
  name: "GreetingCard",
  props: ["greeting"],
  data() {
    return {
      month: "",
      date: "",
      day: "",
      saying: null,
      hours: null,
     
    };
  },
  computed: {
    name(){
      return this.$store.state.name;
    }
  },
  methods: {
    getDate() {
      const weekday = ["日", "一", "二", "三", "四", "五", "六"];
      const now = new Date();
      const month = now.getMonth() + 1;
      const date = now.getDate();
      const day = now.getDay();
      const hours = now.getHours();
      this.month = month;
      this.date = date;
      this.day = weekday[day];
      if (hours > 12) {
        this.hours = "下午";
      } else {
        this.hours = "上午";
      }
    }
  },
  mounted() {
    const jinrishici = require("jinrishici");
    jinrishici.load(result => {
      this.saying = result.data.content;
    });
    this.getDate();
  }
};
</script>