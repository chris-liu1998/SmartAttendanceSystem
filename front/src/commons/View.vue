<template>
  <v-main>
    <!--切换不同的界面-->
    <router-view />

    <dashboard-footer />
  </v-main>
</template>

<script>
export default {
  name: "DashboardView",

  components: {
    // v-footer
    DashboardFooter: () => import("./Footer"),
  },
};
</script>
