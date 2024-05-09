<template>
    <section class="flex flex-col">

        <div class="relative overflow-x-auto shadow-md">
            <table class="w-full text-sm text-left text-gray-400">
                <thead class="text-xs uppercase bg-gray-700 text-gray-400">
                    <tr>
                        <th scope="col" class="px-2 py-3">
                            #
                        </th>
                        <th scope="col" class="pr-6 py-3">
                            Item
                        </th>
                        <th scope="col" class="px-6 py-3">
                            Price
                        </th>
                        <th scope="col" class="px-6 py-3">
                            <span class="sr-only"></span>
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(item, index) in items" :key="index"
                        class="border-b bg-gray-800 border-gray-700 hover:bg-gray-600">
                        <td class="px-2 py-4">
                            {{ index + 1 }}
                        </td>
                        <th scope="row" class="pr-6 py-4 font-medium whitespace-nowrap text-white">
                            <div class="flex items-center gap-2">
                                <div class="md:flex-shrink-0 self-start w-28">
                                    <img class="object-contain"
                                        :src="item.image_url ? item.image_url : '/images/Profile.png'" />
                                </div>
                                <span>
                                    {{ item.title }}
                                </span>
                            </div>
                        </th>
                        <td class="px-6 py-4">
                            <p v-if="(item.discounted_price !== item.price) && (item.discounted_price !== 0)">{{
                                item.discounted_price.toFixed(2) }}$
                            </p>
                            <p v-else>
                                {{ item.price.toFixed(2) }}$
                            </p>
                        </td>
                        <td class="px-6 py-4 text-right">
                            <button @click="dropItem(index)">
                                <a href="#" class="font-medium text-blue-500 hover:underline">Remove</a>
                            </button>
                        </td>
                    </tr>

                </tbody>
                <tfoot>
                    <tr class="font-semibold text-white">
                        <th scope="row" class="px-6 py-3 text-base">Total</th>
                        <td class="px-6 py-3">3</td>
                        <td class="px-6 py-3">{{ sum }}$</td>
                    </tr>
                </tfoot>
            </table>
        </div>


    </section>
</template>

<script setup>
import { computed, ref } from 'vue';

const dropItem = (index) => {
    items.value.splice(index, 1);
}

const items = ref([
    {
        "id": 432706,
        "title": "Lost Summoner Kitty",
        "publication_date": "2018-01-04",
        "developer_name": "Kotoshiro",
        "publisher_name": "Kotoshiro",
        "price": 4.99,
        "discounted_price": 4.49,
        "description": "Monsters appearing one after another. Let's summon a companion who is reliable and get rid of and defeat the enemies by the number of quotas by the time limit.<br>But the enemies are fighting counterattacks, if they are not guarded they will be full of monsters and they will not be able to win.<br>Use the characteristics of your friends and aim for game clear! !<br><br>Monsters do not have money.<br>But if you break the crystal that appears on the stage you will be money!<br>Earn bonus by clearing the stage earlier!<br>You can strengthen your friends by using money.<br><br>All 20 stages without save.<br>Simple play!<br><br>Features of this game<br><ul class=\"bb_ul\"><li>Casual Strategy game easy to play with simple operation<br></li><li>Attack character, collection character, personality character with improved ability<br></li><li>Growth factors that can enhance character<br></li><li>All 20 stages, unexpected volume</li></ul>",
        "image_url": "https://cdn.akamai.steamstatic.com/steam/apps/761140/header.jpg?t=1515115732",
        "app_id": 761140
    },
    {
        "id": 432707,
        "title": "Ironbound",
        "publication_date": "2018-01-04",
        "developer_name": "Secret Level SRL",
        "publisher_name": "Making Fun, Inc.",
        "price": 0,
        "discounted_price": 0,
        "description": "<img src=\"https://cdn.akamai.steamstatic.com/steam/apps/643980/extras/steam3.jpg?t=1696918766\" /><br><br>Sharpen your sword and join the fray in IRONBOUND, the turn-based multiplayer strategy card game where you use your wits to prevail in fast-paced online duels.<br><br>Ironbound is a unique fantasy card game with innovative mechanics and deep online meta-game.<br><br>Online games last between 5 and 10 minutes and reward strategic thinking as well as quick tactical decisions. Familiar, card game gameplay, makes Ironbound easy to pick up, while rich character customization options give you plenty of opportunities to refine your play style and surprise your opponents.<h2 class=\"bb_tag\">KEY FEATURES</h2><ul class=\"bb_ul\"><li>PLAY YOUR OWN WAY<br>You can choose from: a mighty Berserker, a powerful Crusader, a stealthy and deadly Assassin, a magic-wielding Witch or even a reckless Pirate. <br></li><li>DEEP META-GAME<br>With hundreds of weapons, shields and magic trinkets to choose from, there are countless tactics to devise and master in the race to outsmart the other players and rise to the top of the multiplayer ladder.<br></li><li>JOIN THE ARENA<br>In the Arena, the players fight using predefined item sets, ensuring an even playing field regardless of the performance or time spent in ladder games.<br></li><li>CROSS-PLATFORM MULTIPLAYER<br>Ironbound is now available on iOS and Android devices, and you can use a single account to play everywhere. The cross-platform multiplayer is fully supported.</li></ul>",
        "image_url": "https://cdn.akamai.steamstatic.com/steam/apps/643980/header.jpg?t=1696918766",
        "app_id": 643980
    },
])

const sum = computed(() => {
    let sum = 0;
    items.value.forEach(item => {
        if (item.discounted_price == 0 || item.discounted_price == item.price)
            sum += item.price
        else
            sum += item.discounted_price
    });
    return sum;
})
</script>

<style lang="scss" scoped></style>