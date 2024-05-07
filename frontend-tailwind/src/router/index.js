import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
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
      path: "/user",
      name: "user",
      component: () => import("@/views/UserView.vue"),
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
