<template>
    <section>
        <div
            class="grid grid-cols-1 justify-items-center sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 sm:mx-12 md:mx-8 lg:mx-46">
            <GameCard v-for="(game, index) in dummyData" :key="index" :data="game" />

        </div>
    </section>
</template>

<script setup>
import GameCard from '@/components/mainpg/parts/GameCard.vue';
import TransitionTest from '@/components/mainpg/parts/TransitionTest.vue';
import { useGamesStore } from '@/stores/gamesStore';
import { computed, onMounted, ref } from 'vue';

const gamesStore = useGamesStore();

onMounted(async () => {
    // await gamesStore.fetchGames();
})


const dummyData = computed(() => gamesStore.games)


</script>

<style lang="scss" scoped></style>