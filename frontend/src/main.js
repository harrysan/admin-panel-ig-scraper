import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import "bootstrap-icons/font/bootstrap-icons.css";

import { createApp } from "vue";
import router from "./router";

import BaseButton from "./components/ui/BaseButton.vue";
import BaseOption from "./components/ui/BaseOption.vue";
import BaseSpinner from "./components/ui/BaseSpinner.vue";

import App from "./App.vue";

const app = createApp(App);

app.use(router);

app.component("base-button", BaseButton);
app.component("base-option", BaseOption);
app.component("base-spinner", BaseSpinner);

app.mount("#app");
