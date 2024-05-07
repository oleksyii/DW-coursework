// cartStore.js
import { defineStore } from "pinia";
import { ref } from "vue";

export const useCartStore = defineStore("cartStore", () => {
  const cartItems = ref([]);

  function pushItem(game) {
    cartItems.value.push(game);
  }

  function dropItem(index) {
    cartItems.value.splice(index, 1);
  }

  return {
    cartItems,
    pushItem,
    dropItem,
  };
});
