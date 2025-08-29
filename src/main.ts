import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import {createRouter, createWebHistory} from 'vue-router'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            component: () => import("./Views/Search.vue"),
            name: "searh",
            path: "/",
            meta: {title: "Search"}
        },
        {
            component: () => import("./Views/SearchResult.vue"),
            name: "results",
            path: "/results/",
            meta: {title: "Results"}
        }
    ]
});


router.afterEach((to, _from, _failure) => {
    const title = (to.meta?.title as string) ?? "Search Engine";
    document.title = title;
})

createApp(App)
    .use(router)
    .mount('#app')
