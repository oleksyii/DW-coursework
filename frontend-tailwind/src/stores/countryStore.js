// countryStore.js
import { defineStore } from "pinia";
import { ref } from "vue";

export const useCountryStore = defineStore("usersStore", () => {
  const countries = ref([]);

  async function fetchCountriesData1(store) {
    const response = await fetch(`http://127.0.0.1:8000/countries`);
    if (response.ok) {
      store.countries = await response.json();
    } else {
      console.error("HTTP-Error: " + response.status);
    }
  }

  return {
    countries,
    fetchCountriesData1,
  };
});
