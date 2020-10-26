<template>
  <v-card class="ma-3" max-width="300" height="180">
    <v-list-item>
      <v-list-item-avatar tile size="100" rounded class="mt-n8">
        <v-sheet color="blue lighten-3" width="70" height="70" elevation="5" rounded>
          <v-icon dark large>fas fa-cloud</v-icon>
        </v-sheet>
      </v-list-item-avatar>
      <v-col class="display-2" cols="6">23&deg;C</v-col>
    </v-list-item>
    <v-list-item two-line>
      <v-col class="pa-0">
        <v-list-item-content>
          <v-list-item-title class="headline">烟台市</v-list-item-title>
          <v-list-item-subtitle>{{hour}}:{{min}} {{pmam}},  多云</v-list-item-subtitle>
        </v-list-item-content>
      </v-col>
      <v-col>
        <v-img src="../../assets/cloudy_day.png" width="70" height="70" class="ml-3"></v-img>
      </v-col>
    </v-list-item>
  </v-card>
</template>

<script>
export default {
  name: "WeatherCard",
  data() {
    return {
      labels: ["SU", "MO", "TU", "WED", "TH", "FR", "SA"],
      time: 0,
      hour: "12",
      min: "02",
      pmam: "PM",
      forecast: [
        {
          day: "Tuesday",
          icon: "mdi-white-balance-sunny",
          temp: "24\xB0/12\xB0",
        },
        {
          day: "Wednesday",
          icon: "mdi-white-balance-sunny",
          temp: "22\xB0/14\xB0",
        },
        { day: "Thursday", icon: "mdi-cloud", temp: "25\xB0/15\xB0" },
      ],
    };
  },
  mounted() {
    this.getTime();
  },
  methods: {
    getTime() {
      const now = new Date();
      let h = now.getHours();
      let mm = now.getMinutes();
      if(h > 12){
          this.pmam = "PM";
          h -= 12;
      }else{
          this.pmam = "AM";
      }
      this.hour = h;
      this.min = mm;
    },
  },
};
</script>

<style>
</style>