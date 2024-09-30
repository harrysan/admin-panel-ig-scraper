import { createRouter, createWebHistory } from "vue-router";

import DashboardPage from "./pages/dashboard/DashboardPage.vue";
import FeedbackPage from "./pages/feedback/FeedbackPage.vue";
import UsersPage from "./pages/users/UsersPage.vue";
import NotFound from "./pages/NotFound.vue";
import UserDetail from "./pages/users/UserDetail.vue";
import UserPosts from "./pages/users/UserPosts.vue";
import UserStories from "./pages/users/UserStories.vue";
import UserMenu from "./pages/users/UserMenu.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/dashboard", meta: { title: "Scraper Dashboard" } },
    {
      path: "/dashboard",
      component: DashboardPage,
      meta: { title: "Scraper Dashboard" },
    },
    {
      path: "/users",
      component: UsersPage,
      meta: { title: "Scraper Dashboard - User" },
    },
    {
      path: "/users/:id",
      component: UserMenu,
      props: true,
      children: [
        { path: "posts", component: UserPosts, props: true },
        { path: "story", component: UserStories, props: true },
        { path: "detail", component: UserDetail, props: true },
      ],
      meta: { title: "Scraper Dashboard - Posts" },
    },
    {
      path: "/feedback",
      component: FeedbackPage,
      meta: { title: "Scraper Dashbord - Feedback" },
    },
    { path: "/:notFound(.*)", component: NotFound },
  ],
});

export default router;
