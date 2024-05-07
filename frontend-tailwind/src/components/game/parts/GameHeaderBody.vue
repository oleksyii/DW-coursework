<template>
    <section class="flex justify-center">
        <div class="flex flex-col gap-5 text-wrap divide-y divide-solid">
            <div class="flex gap-2">
                <img class="object-contain " :src="game.image_url" alt="">
                <div class="min-w-46 flex flex-col gap-3">
                    <h2 class="text-4xl font-bold">{{ game.title }}</h2>
                    <div class="grid grid-cols-2">
                        <span class="text-gray-500 font-semibold uppercase text-sm ">RELEASE DATE:</span>
                        <span class="text-blue-cart font-semibold hover:text-white">{{ game.publication_date }}:</span>
                    </div>
                    <div class="grid grid-cols-2 min-w-72">
                        <span class="text-gray-500 font-semibold uppercase text-sm ">Publisher:</span>
                        <span class="text-blue-cart font-semibold hover:text-white">{{ game.publisher_name }}</span>
                        <span class="text-gray-500 font-semibold uppercase text-sm">Developer:</span>
                        <span class="text-blue-cart font-semibold hover:text-white">{{ game.developer_name }}</span>
                    </div>
                    <div>
                        <p class="text-gray-500 font-semibold text-sm">Genres:</p>
                        <div class="flex gap-1">
                            <Genre v-for="(genre, index) in game.genres" :key="index" :label="genre" />
                        </div>
                    </div>
                </div>
            </div>
            <div class="flex flex-col divide-y pt-5">
                <p v-html="game.description"></p>
            </div>
        </div>
    </section>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import Genre from './Genre.vue';

onMounted(() => {
    console.log(game.value)
})

const props = defineProps({
    game: {
        type: Object,
        require: true
    },
})

const game = computed(() => props.game)

watch(() => game, (newValue, oldValue) => {
    console.log('the values changed: ', oldValue, newValue);
})

</script>

<style lang="scss">
.bb_tag {
    font-weight: bold;
    color: #2F89BC;
}

/* Define styles for unordered lists */
.bb_ul {
    list-style-type: disc;
    /* Use dots for list items */
}

/* Define styles for list items */
.bb_ul li {
    margin-left: 1rem;
    /* Add some margin for better readability */
}
</style>