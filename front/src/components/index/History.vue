<template>
  <v-card width="auto" class="ma-3" height="180">
    <v-list-item>
      <v-list-item-avatar tile size="100" rounded class="mt-n8 mr-0 mb-0">
        <v-sheet color="purple lighten-3" width="70" height="70" elevation="5" rounded>
          <v-icon dark large>fas fa-history</v-icon>
        </v-sheet>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-subtitle class="grey--text">上次打卡：{{history}}</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title>距离下次打卡：</v-list-item-title>
        <v-row class="pa-0 fill-height">
          <v-col class="text-h3">{{min}}:{{sec}}</v-col>
          <v-col>
            <v-btn
              color="red"
              dark
              retain-focus-on-click
              fab
              large
              class="mt-n3"
              @click="jump"
            >
              <v-icon>fas fa-camera</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-list-item-content>
    </v-list-item>
  </v-card>
</template>

<script>
export default {
  name: "History",
  data() {
    return {
      history: "08:21",
      min: "08",
      sec: "05",
    };
  },
  mounted() {},
  methods: {
    jump() {
      let path = "attendance/facerecord";
      this.$router.push(path);
    },
  },
};
</script>

<style>
</style>