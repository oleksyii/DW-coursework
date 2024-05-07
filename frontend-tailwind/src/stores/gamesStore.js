// gamesStore.js
import { defineStore } from "pinia";
import { ref } from "vue";

export const useGamesStore = defineStore("gamesStore", () => {
  const games = ref([
    {
      id: 432706,
      title: "Lost Summoner Kitty",
      publication_date: "2018-01-04",
      developer_name: "Kotoshiro",
      publisher_name: "Kotoshiro",
      price: 4.99,
      discounted_price: 4.49,
      description:
        'Monsters appearing one after another. Let\'s summon a companion who is reliable and get rid of and defeat the enemies by the number of quotas by the time limit.<br>But the enemies are fighting counterattacks, if they are not guarded they will be full of monsters and they will not be able to win.<br>Use the characteristics of your friends and aim for game clear! !<br><br>Monsters do not have money.<br>But if you break the crystal that appears on the stage you will be money!<br>Earn bonus by clearing the stage earlier!<br>You can strengthen your friends by using money.<br><br>All 20 stages without save.<br>Simple play!<br><br>Features of this game<br><ul class="bb_ul"><li>Casual Strategy game easy to play with simple operation<br></li><li>Attack character, collection character, personality character with improved ability<br></li><li>Growth factors that can enhance character<br></li><li>All 20 stages, unexpected volume</li></ul>',
      image_url:
        "https://cdn.akamai.steamstatic.com/steam/apps/761140/header.jpg?t=1515115732",
      app_id: 761140,
      genres: ["Action", "Casual", "Indie", "Simulation", "Strategy"],
    },
    {
      id: 432707,
      title: "Ironbound",
      publication_date: "2018-01-04",
      developer_name: "Secret Level SRL",
      publisher_name: "Making Fun, Inc.",
      price: 0,
      discounted_price: 0,
      description:
        '<img src="https://cdn.akamai.steamstatic.com/steam/apps/643980/extras/steam3.jpg?t=1696918766" /><br><br>Sharpen your sword and join the fray in IRONBOUND, the turn-based multiplayer strategy card game where you use your wits to prevail in fast-paced online duels.<br><br>Ironbound is a unique fantasy card game with innovative mechanics and deep online meta-game.<br><br>Online games last between 5 and 10 minutes and reward strategic thinking as well as quick tactical decisions. Familiar, card game gameplay, makes Ironbound easy to pick up, while rich character customization options give you plenty of opportunities to refine your play style and surprise your opponents.<h2 class="bb_tag">KEY FEATURES</h2><ul class="bb_ul"><li>PLAY YOUR OWN WAY<br>You can choose from: a mighty Berserker, a powerful Crusader, a stealthy and deadly Assassin, a magic-wielding Witch or even a reckless Pirate. <br></li><li>DEEP META-GAME<br>With hundreds of weapons, shields and magic trinkets to choose from, there are countless tactics to devise and master in the race to outsmart the other players and rise to the top of the multiplayer ladder.<br></li><li>JOIN THE ARENA<br>In the Arena, the players fight using predefined item sets, ensuring an even playing field regardless of the performance or time spent in ladder games.<br></li><li>CROSS-PLATFORM MULTIPLAYER<br>Ironbound is now available on iOS and Android devices, and you can use a single account to play everywhere. The cross-platform multiplayer is fully supported.</li></ul>',
      image_url:
        "https://cdn.akamai.steamstatic.com/steam/apps/643980/header.jpg?t=1696918766",
      app_id: 643980,
      genres: ["Free to Play", "Indie", "RPG", "Strategy"],
    },
    {
      id: 480759,
      title: "Half-Life",
      publication_date: "1998-11-08",
      developer_name: "Valve",
      publisher_name: "Valve",
      price: 9.99,
      discounted_price: 0,
      description:
        "Named Game of the Year by over 50 publications, Valve's debut title blends action and adventure with award-winning technology to create a frighteningly realistic world where players must think to survive. Also includes an exciting multiplayer mode that allows you to play against friends and enemies around the world.",
      image_url:
        "https://cdn.akamai.steamstatic.com/steam/apps/70/header.jpg?t=1700269108",
      app_id: 70,
      genres: ["Action"],
    },
  ]);

  async function fetchGames() {
    //TODO: localhost/games/{page}
    const response = await fetch(`http://127.0.0.1:8000/metadata`);
    if (response.ok) {
      this.games = await response.json();
    } else {
      console.error("HTTP-Error: " + response.status);
    }
  }

  async function fetchGame(id) {
    //TODO fetch the localhost/game{id}
    const res = games.value.find((game) => game.id === parseInt(id));
    return res;
  }

  async function fetchReviews(game_id) {}

  return {
    games,
    fetchGames,
    fetchGame,
  };
});
