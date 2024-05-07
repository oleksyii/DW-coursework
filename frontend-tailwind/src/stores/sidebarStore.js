// sidebarStore.js
import { defineStore } from "pinia";
import { ref } from "vue";

export const useSidebarStore = defineStore("sidebarStore", () => {
  const isSidebarOpen = ref(false);

  function setSidebarOpenStatus(status) {
    isSidebarOpen.value = status;
  }
  function toggleSidebar() {
    isSidebarOpen.value = !isSidebarOpen.value;
  }

  return {
    setSidebarOpenStatus,
    toggleSidebar,
    isSidebarOpen,
  };
});
