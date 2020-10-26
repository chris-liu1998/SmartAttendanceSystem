<template>
  <v-app>
    <Navbar />
    <dashboard-view class="grey lighten-4"/>
  </v-app>
</template>

<script>
export default {
  name: "DashboardLayout",
  components: {
    Navbar: () => import("./Nav"),
    DashboardView: () => import("./View"),
  },
};
</script>
