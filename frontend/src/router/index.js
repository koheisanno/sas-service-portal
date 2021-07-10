import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Clubs from "../views/Clubs.vue";
import ClubPage from "../views/ClubPage.vue";
import Dashboard from "../views/Dashboard.vue";
import Join from "../views/Join.vue";
import Leave from "../views/Leave.vue";
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
    path: "/dashboard/",
    name: "Dashboard",
    component: Dashboard,
  },
  {
    path: "/join/:id",
    name: "Join",
    component: Join,
    props: true,
  },
  {
    path: "/leave/:id",
    name: "Leave",
    component: Leave,
    props: true,
  },
  {
    path: "/checkin/:id",
    name: "Check-in",
    component: Checkin,
    props: true,
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
