import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      redirect: "/games/1",
      // name: "home",
      // component: HomeView,
    },
    {
      path: "/games/:page",
      name: "home",
      component: HomeView,
    },
    {
      path: "/game/:id",
      component: () => import("@/views/GamePageView.vue"),
    },
    {
      path: "/about",
      name: "about",
      component: () => import("../views/AboutView.vue"),
    },
    {
      path: "/users",
      name: "users",
      component: () => import("@/views/UserView.vue"),
    },
    {
      path: "/orders",
      name: "orders",
      component: () => import("@/views/OrderView.vue"),
    },
    {
      path: "/reviews",
      name: "reviews",
      component: () => import("@/views/ReviewView.vue"),
    },
    {
      path: "/export",
      name: "export",
      component: () => import("@/views/ExportView.vue"),
    },
    {
      path: "/bi",
      name: "bi",
      component: () => import("@/views/BIView.vue"),
    },
    {
      path: "/modal-sample",
      name: "modal_sample",
      component: () => import("@/components/samples/ModalSample.vue"),
    },
    {
      path: "/upload-image-sample",
      name: "upload_image_sample",
      component: () => import("@/views/UploadImageView.vue"),
    },
  ],
});

export default router;
