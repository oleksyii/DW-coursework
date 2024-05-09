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

  // TODO: fetch the specific user's review

  async function fetchAllReviews({
    order_by = "posted_date",
    order_direction = "ASC",
    num = 100,
    game_name = null,
    date_from = null,
    date_to = null,
    is_only_interacted = null,
  }) {
    
    let url = `http://127.0.0.1:8000/reviews?order_by=${order_by}&order_direction=${order_direction}&num=${num}`;
    
    if (game_name) {
      url += `&game_name=${game_name}`;
    }
    if (date_from && !date_to) {
      url += `&date_from=${date_from}`;
    }
    if (date_from && date_to) {
      url += `&date_from=${date_from}&date_to=${date_to}`;
    }
    if (is_only_interacted) {
      url += `&is_only_interacted=${is_only_interacted}`;
    }

    console.log(`The URL is ${url}`);

    const response = await fetch(url);
    if (response.ok) {
      this.reviews = await response.json();
    } else {
      console.error("HTTP-Error: " + response.status);
    }
    console.log(reviews);
  }

  return {
    reviews,
    fetchReviews,
    fetchAllReviews,
  };
});
