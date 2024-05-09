<template>
    <section
        class="m-6 bg-gray-middle hover:bg-gray-light shadow-2xl max-w-sm sm:w-52 md:w-72 transition delay-200 hover:-translate-y-1 hover:scale-110 duration-300">
        <div class="flex flex-col relative h-full group game-card">
            <div
                class="absolute hidden group-hover:inline-block top-1 right-2 bg-gray-superlight rounded-sm p-1 h-7 hover:bg-blue-cart">
                <button class="">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                        stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="10" cy="20.5" r="1" />
                        <circle cx="18" cy="20.5" r="1" />
                        <path d="M2.5 2.5h3l2.7 12.4a2 2 0 0 0 2 1.6h7.7a2 2 0 0 0 2-1.6l1.6-8.4H7.1" />
                    </svg>
                </button>
            </div>
            <div class="md:flex-shrink-0 self-start">
                <img class="object-contain" :src="game.image_url ? game.image_url : '/images/Profile.png'" />
            </div>
            <div class="text-start text-nowrap overflow-hidden flex flex-col justify-between h-full">
                <router-link :to="`/game/`+game.id">
                    <p class="font-semibold text-3xl mx-1 mb-1 grow content-center">
                        {{ game.title }}
                    </p>
                </router-link>
                <div class="bg-my-green-hover hover:bg-my-green hover:text-white flex justify-between px-1">
                    <div class="bg-gray-price px-0.5 my-0.5 text-sm flex">
                        <div
                            :class="{ 'line-through': (game.discounted_price !== game.price) && (game.discounted_price !== 0) }">
                            <p v-if="game.price > 0" class="font-semibold">{{ game.price }}$</p>
                            <p v-else class="font-semibold">Free</p>
                        </div>
                        <div v-if="(game.discounted_price !== game.price) && (game.discounted_price !== 0.00)"
                            class="bg-gray-price text-green-price ms-0.5 text-sm">
                            <p class="font-semibold">{{ game.discounted_price }}$</p>
                        </div>
                    </div>

                    <button class="hover:underline">
                        <span class="font-semibold">Buy Now</span>
                    </button>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const props = defineProps({
    data: {
        type: Object,
        require: true,
    },
});

const game = computed(() => props.data);

</script>

<style lang="scss" scoped></style>