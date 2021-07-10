import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

import PrimeVue from "primevue/config";

import ToastService from "primevue/toastservice";

import "primevue/resources/themes/fluent-light/theme.css"; //theme
import "primevue/resources/primevue.min.css"; //core css
import "primeicons/primeicons.css"; //icons

import "bootstrap/dist/css/bootstrap.min.css";

let app = createApp(App);
app.use(PrimeVue);
app.use(router);
app.use(ToastService);

app.mount("#app");