  // usersStore.js
  import { defineStore } from "pinia";
  import { ref } from "vue";

  export const useUserStore = defineStore("usersStore", () => {
    const users = ref([]);

    async function fetchUserData({
      order_by = "name",
      order_direction = "ASC",
      num = 100,
    }) {
      console.log(`printing bt ${order_by}`);
      const response = await fetch(
        `http://127.0.0.1:8000/users?order_by=${order_by}&order_direction=${order_direction}&num=${num}`
      );
      if (response.ok) {
        this.users = await response.json();
      } else {
        console.error("HTTP-Error: " + response.status);
      }
      console.log(users);
    }

    return {
      users,
      fetchUserData,
    };
  });
