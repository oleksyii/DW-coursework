import "./assets/main.css";

import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { createPinia } from "pinia";

import Vue3Toasity from "vue3-toastify";
import "vue3-toastify/dist/index.css";

// Create a new Pinia instance
const pinia = createPinia();

const app = createApp(App);

app.use(router);
// Use the Pinia plugin
app.use(pinia);

app.mount("#app");
