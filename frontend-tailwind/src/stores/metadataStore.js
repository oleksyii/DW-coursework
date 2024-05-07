// countryStore.js
import { defineStore } from "pinia";
import { ref } from "vue";

export const useMetadataStore = defineStore("metadataStore", () => {
  const metadata = ref({});

  async function fetchMetadata() {
    const response = await fetch(`http://127.0.0.1:8000/metadata`);
    if (response.ok) {
      this.metadata = await response.json();
    } else {
      console.error("HTTP-Error: " + response.status);
    }
  }
  return {
    metadata,
    fetchMetadata,
  };
});
