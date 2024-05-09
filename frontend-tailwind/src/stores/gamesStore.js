// gamesStore.js
import { defineStore } from "pinia";
import { ref } from "vue";

export const useGamesStore = defineStore("gamesStore", () => {
  const activeUser = ref("76561197970982479");
  const isSignedIn = ref(true);
  const isAdmin = ref(false);
  const page = ref(1);
  const games = ref();

  async function fetchGames(fetchPage) {
    if (isSignedIn.value) {
      const response = await fetch(
        `http://127.0.0.1:8000/games/${fetchPage}?username=${activeUser.value}`
      );
      if (response.ok) {
        let res = await response.json();
        this.games = res.payload;
        this.page = fetchPage;
      } else {
        console.error("HTTP-Error: " + response.status);
      }
    } else {
      const response = await fetch(`http://127.0.0.1:8000/games/${fetchPage}`);
      if (response.ok) {
        let res = await response.json();
        this.games = res.payload;
        this.page = fetchPage;
      } else {
        console.error("HTTP-Error: " + response.status);
      }
    }
  }

  async function fetchGame(id) {
    //TODO fetch the localhost/game{id}
    const res = games.value.find((game) => game.id === parseInt(id));
    return res;
  }

  async function setPage(page) {
    this.page = page;
  }

  async function fetchGamesNames() {
    const response = await fetch(`http://127.0.0.1:8000/games/${fetchPage}`);
    if (response.ok) {
      let res = await response.json();
      this.games = res.payload;
      this.page = fetchPage;
    } else {
      console.error("HTTP-Error: " + response.status);
    }
  }

  return {
    activeUser,
    isAdmin,
    isSignedIn,
    games,
    page,
    fetchGames,
    fetchGame,
    setPage,
  };
});
