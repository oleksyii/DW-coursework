// reviewsStore.js
import { defineStore } from "pinia";
import { ref } from "vue";

export const useReviewsStore = defineStore("reviewsStore", () => {
  const reviews = ref([]);

  async function fetchReviews(game_id) {
    console.log(`fetching the reviews, teh game_id is: ${game_id}`);
    const response = await fetch(`http://127.0.0.1:8000/reviews/${game_id}`);
    if (response.ok) {
      this.reviews = await response.json();
    } else {
      console.error("HTTP-Error: " + response.status);
    }
  }

  // TODO: fetch the user's review

  return {
    reviews,
    fetchReviews,
  };
});
