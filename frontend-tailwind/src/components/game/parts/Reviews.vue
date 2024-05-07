<template>
    <section class="flex justify-center">
        <div class="flex flex-col w-2/3 gap-2">
            <div v-for="(review, index) in reviews" :key="index" class="bg-black-review text-wrap">
                <div>
                    {{ review.name }}
                </div>
                <div>
                    {{ review.posted_date }}
                </div>
                <div>
                    {{ review.review_text }}
                </div>
                <div class="flex flex-col">
                    <div class="flex gap-1">
                        <button class="bg-blue-cart">
                            <IconLike />
                        </button>
                        <button class="bg-red-dislike">
                            <IconDislike />
                        </button>
                    </div>
                    <div>
                        {{ review.funny_count }} found this review funny
                    </div>
                    <div>
                        {{ review.useful_count }} found this review helpful
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup>
import { computed, onMounted, watch, ref } from 'vue';
import { useReviewsStore } from '@/stores/reviewsStore';
import IconLike from '@/components/icons/IconLike.vue';
import IconDislike from '@/components/icons/IconDislike.vue';

const reviewsStore = useReviewsStore();

const reviews = ref([]);
// const revs = ref([])

const props = defineProps({
    game_id: {
        type: Number,
        require: true
    },
})

const game_id = computed(() => props.game_id)

watch(game_id, (newvalue, oldValue) => {
    console.log('newValue, oldValue', newvalue, oldValue);
    reviewsStore.fetchReviews(game_id.value).then(() => {
        console.log("happilly getched the data ", reviewsStore.reviews);
        reviews.value = reviewsStore.reviews;
        console.log(reviews.value);
    })
})

onMounted(async () => {
    console.log("Hello", game_id.value, reviewsStore.reviews)
    // await reviewsStore.fetchReviews(game_id.value)
})

</script>

<style lang="scss" scoped></style>