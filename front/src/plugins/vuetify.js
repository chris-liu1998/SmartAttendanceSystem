import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import '@fortawesome/fontawesome-free/css/all.css'
// import colors from 'vuetify/lib/util/colors'
import zhHans from 'vuetify/es5/locale/zh-Hans';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: "#495057",
      },
    },
  },
  icons: {
    iconfont: 'md' || 'mdi' || 'fa',	// 设置使用本地的icon资源
  },
  lang: {
    locales: { zhHans },
    current: 'zhHans',
  }
});
