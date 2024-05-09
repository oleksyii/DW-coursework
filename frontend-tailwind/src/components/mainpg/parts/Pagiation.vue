<template>
    <section>


        <div class="flex">
            <!-- Previous Button -->
            <a :href="`/games/${(parseInt(gamesStore.page) - 1)}`"
                class="flex items-center justify-center px-3 h-8 w-28 me-3 text-sm font-medium border rounded-lg bg-gray-800 border-gray-700 text-gray-400 hover:bg-gray-700 hover:text-white">
                <svg class="w-3.5 h-3.5 me-2 rtl:rotate-180" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
                    fill="none" viewBox="0 0 14 10">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M13 5H1m0 0 4 4M1 5l4-4" />
                </svg>
                Previous
            </a>
            <a :href="`/games/` + (parseInt(gamesStore.page) + 1)"
                class="flex items-center justify-center px-3 h-8 w-28 text-sm font-medium border rounded-lg bg-gray-800 border-gray-700 text-gray-400 hover:bg-gray-700 hover:text-white">
                Next
                <svg class="w-3.5 h-3.5 ms-2 rtl:rotate-180" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
                    fill="none" viewBox="0 0 14 10">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M1 5h12m0 0L9 1m4 4L9 9" />
                </svg>
            </a>
        </div>
    </section>
</template>

<script setup>
import { onMounted } from "vue";
import { initFlowbite } from 'flowbite'
import { useGamesStore } from "@/stores/gamesStore";
import { useRouter, useRoute } from 'vue-router';

const gamesStore = useGamesStore()
const route = useRoute();
const router = useRouter();

const refreshPage = () => {
    // Extract the page number from the current route and decrement it by 1
    const pageNumber = parseInt(route.params.page) - 1;

    gamesStore.setPage(pageNumber)

    // Navigate to the modified route, effectively refreshing the page
    router.push({ path: `/games/${pageNumber}` });
    // window.location.reload()
};

onMounted(() => {
    initFlowbite();
})
</script>

<style lang="scss" scoped></style>