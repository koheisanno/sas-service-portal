import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Clubs from "../views/Clubs.vue";
import ClubPage from "../views/ClubPage.vue";
import Dashboard from "../views/Dashboard.vue";
import Join from "../views/Join.vue";
import Checkin from "../views/Check-in.vue";
import PageNotFound from "../views/PageNotFound.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/clubs",
    name: "Clubs",
    component: Clubs,
  },
  {
    path: "/clubs/:id",
    name: "ClubPage",
    component: ClubPage,
    props: true,
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: Dashboard,
  },
  {
    path: "/join",
    name: "Join",
    component: Join,
    props: route => ({ query: route.query.id })
  },
  {
    path: "/checkin",
    name: "Check-in",
    component: Checkin,
    props: route => ({ query: route.query.id })
  },
  {
    path: "/:catchAll(.*)",
    name: "Page-not-found",
    component: PageNotFound,
  },
];

const router = createRouter({
  //history: createWebHistory(process.env.BASE_URL),
  history: createWebHistory(),
  routes,
});

export default router;