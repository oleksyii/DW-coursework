<template>
    <section class="flex justify-center mt-4">
        <div class=" w-7/12 flex flex-col divide-y divide-solid justify-center gap-5">
            <GameHeader :game="computedGame" />
            <p class="pt-5">some text</p>
            <Reviews class="pt-5" :game_id="computedGame.id" />
        </div>

    </section>
</template>

<script setup>
import { onMounted, ref, onBeforeMount, computed } from "vue";
import { useRoute, useRouter } from 'vue-router';
import { useGamesStore } from '@/stores/gamesStore'
import GameHeader from "@/components/game/parts/GameHeaderBody.vue";
import Reviews from "./parts/Reviews.vue";

const router = useRouter();
const route = useRoute();

const gamesStore = useGamesStore()

const game = ref({})

onBeforeMount(async () => {
    const game_id = route.params.id;
    if (game_id?.length) {
        gamesStore.fetchGame(game_id).then((data) => {
            game.value = { ...data };
            console.log(game.value);
        });

    }
})

const computedGame = computed(() => game.value)
</script>

<style lang="scss" scoped></style>