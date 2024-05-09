// usersStore.js
import { defineStore } from "pinia";
import { ref } from "vue";

export const useOrdersStore = defineStore("orderStore", () => {
  const orders = ref([]);

  async function fetchOrderData({
    order_by = "order_date",
    order_direction = "ASC",
    num = 100,
    date_from = null,
    date_to = null,
    status = null,
  }) {
    console.log(`printing by ${order_by}`);

    let url = `http://127.0.0.1:8000/orders?order_by=${order_by}&order_direction=${order_direction}&num=${num}`;

    if (date_from)
      url += `&date_from=${date_from}`
    if (date_from && date_to)
      url += `&date_from=${date_from}&date_to=${date_to}`
    if (status)
      url += `&status=${status.toString()}`;

    console.log(url);

    const response = await fetch(
      url
    );
    if (response.ok) {
      this.orders = await response.json();
    } else {
      console.error("HTTP-Error: " + response.status);
    }
    console.log(orders);
  }

  return {
    orders,
    fetchOrderData,
  };
});
