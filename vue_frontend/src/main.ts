import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

//import App from './App.vue'
import Main from './Main.vue'
import router from './router'

import './assets/main.css'

//const app = createApp(App)
const app = createApp(Main)
app.provide("backend_host", import.meta.env.VITE_BACKEND_HOST)
app.use(createPinia())
app.use(router)
//app.use(ElementPlus, { size: 'small', zIndex: 3000 })
app.use(ElementPlus)
//app.component('EasyDataTable', Vue3EasyDataTable);

app.mount('#main')
