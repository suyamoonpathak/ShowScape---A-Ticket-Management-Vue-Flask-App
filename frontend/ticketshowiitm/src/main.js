import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "@fortawesome/fontawesome-free/css/all.css";
import CanvasJSChart from "@canvasjs/vue-charts";

createApp(App).use(router).use(CanvasJSChart).mount("#app");
