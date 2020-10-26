<template>
  <v-footer id="dashboard-footer" app inset width="auto" height="50">
    <v-container>
      <v-row align="center" no-gutters>
        <v-spacer class="hidden-sm-and-down" />

        <v-col cols="12" md="auto">
          <div class="body-1 font-weight-light pt-6 pt-md-0 text-center">
            &copy; 2020, made with
            <v-icon size="18">mdi-heart</v-icon>
            by <a href="http://39.98.127.39:3000/group25/IAS.git">25组</a>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script>
  export default {
    name: 'DashboardFooter',
  }
</script>


