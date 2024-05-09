<template>
    <section class="flex flex-col gap-9">
        <div
            class="grid grid-cols-1 justify-items-center sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 sm:mx-12 md:mx-8 lg:mx-46 max-w-full">
            <GameCard v-for="(game, index) in games" :key="index" :data="game" />

        </div>
        <div class="flex justify-center items-center">
            <Pagiation />
        </div>
    </section>
</template>

<script setup>
import GameCard from '@/components/mainpg/parts/GameCard.vue';
import TransitionTest from '@/components/mainpg/parts/TransitionTest.vue';
import Pagiation from '@/components/mainpg/parts/Pagiation.vue';
import { useGamesStore } from '@/stores/gamesStore';
import { computed, onMounted, ref, watch, onBeforeMount } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const router = useRouter();
const route = useRoute();

const gamesStore = useGamesStore();

const page = ref(1);

onMounted(async () => {
    await gamesStore.fetchGames(page.value);
})

watch(page, async (newValue, oldValue) => {
    await gamesStore.fetchGames(page.value)
})

watch(route.params.page, async (newValue, oldValue) => {
    console.log('The page was changed: ', newValue, oldValue);
    page.value = gamesStore.page;
    await gamesStore.fetchGames(page.value)
})

onBeforeMount(async () => {
    page.value = route.params.page;
    if (page?.length) {
        gamesStore.setPage(page.value).then(() => {
            console.log(page.value);
            // if (page.value) {
            //     router.push({ path: `/games/${page.value}` });
            // }
        });

    }
})


const games = computed(() => gamesStore.games)

watch(games, (newValue, oldValue) => {
    console.log('Gathered new games: ', newValue, oldValue)
})


</script>

<style lang="scss" scoped></style>