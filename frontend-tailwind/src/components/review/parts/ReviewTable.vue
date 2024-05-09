<template>
    <section>
        <table class="w-full text-sm text-left rtl:text-right text-gray-400">
            <thead class="text-xs  uppercase bg-gray-700 text-gray-400">
                <tr>
                    <th scope="col" class="px-6 py-3">
                        <button class="uppercase" @click="toggleSortDirection('name')">
                            Name
                            <span v-if="sortField === 'name'" class="ml-1">
                                <span v-if="sortDirection === 'ASC'">▲</span>
                                <span v-else>▼</span>
                            </span>
                        </button>
                    </th>
                    <th scope="col" class="text-center py-3 ">
                        <button class="uppercase" @click="toggleSortDirection('username')">
                            Username
                            <span v-if="sortField === 'username'" class="ml-1">
                                <span v-if="sortDirection === 'ASC'">▲</span>
                                <span v-else>▼</span>
                            </span>
                        </button>
                    </th>
                    <th scope="col" class="text-center px-9 py-3">
                        <button class="uppercase" @click="toggleSortDirection('game')">
                            <div class="flex">
                                Game
                                <span v-if="sortField === 'game'" class="ml-1">
                                    <span v-if="sortDirection === 'ASC'">▲</span>
                                    <span v-else>▼</span>
                                </span>
                            </div>
                        </button>
                    </th>
                    <th scope="col" class="text-center px-6 py-3">
                        <button class="uppercase" @click="toggleSortDirection('posted_date')">
                            <div class="flex">
                                Posted date
                                <span v-if="sortField === 'posted_date'" class="ml-1">
                                    <span v-if="sortDirection === 'ASC'">▲</span>
                                    <span v-else>▼</span>
                                </span>
                            </div>
                        </button>
                    </th>
                    <th scope="col" class="text-center px-3 py-3">
                        <button class="uppercase" @click="toggleSortDirection('funny_count')">
                            <div class="flex">
                                Funny count
                                <span v-if="sortField === 'funny_count'" class="ml-1">
                                    <span v-if="sortDirection === 'ASC'">▲</span>
                                    <span v-else>▼</span>
                                </span>
                            </div>
                        </button>
                    </th>
                    <th scope="col" class="text-center px-3 py-3">
                        <button class="uppercase" @click="toggleSortDirection('useful_count')">
                            <div class="flex">
                                Useful count
                                <span v-if="sortField === 'useful_count'" class="ml-1">
                                    <span v-if="sortDirection === 'ASC'">▲</span>
                                    <span v-else>▼</span>
                                </span>
                            </div>
                        </button>
                    </th>
                    <th scope="col" class="text-center px-3 py-3">
                        <button class="uppercase" @click="toggleSortDirection('interactions_count')">
                            <div class="flex">
                                Interactions count
                                <span v-if="sortField === 'interactions_count'" class="ml-1">
                                    <span v-if="sortDirection === 'ASC'">▲</span>
                                    <span v-else>▼</span>
                                </span>
                            </div>
                        </button>
                    </th>
                    <th scope="col" class="text-center px-3 py-3">
                        <button class="uppercase" @click="toggleSortDirection('recommend')">
                            <div class="flex">
                                Recommend
                                <span v-if="sortField === 'recommend'" class="ml-1">
                                    <span v-if="sortDirection === 'ASC'">▲</span>
                                    <span v-else>▼</span>
                                </span>
                            </div>
                        </button>
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(review, index) in store.reviews" :key="index"
                    class="odd:bg-gray-900 even:bg-gray-800 border-b border-gray-700">
                    <td scope="row" class="px-6 py-4 font-medium whitespace-nowrap text-white">
                        {{ review.name }}
                    </td>
                    <td class=" py-4">
                        {{ review.username }}
                    </td>
                    <td class="px-3 py-4">
                        {{ review.game }}
                    </td>
                    <td class="px-3 py-4 text-center">
                        {{ review.posted_date }}
                    </td>
                    <td class="px-2 py-4 text-center">
                        {{ review.funny_count }}
                    </td>
                    <td class="px-2 py-4 text-center">
                        {{ review.useful_count }}
                    </td>
                    <td class="px-2 py-4 text-center">
                        {{ review.interactions_count }}
                    </td>
                    <td class="px-2 py-4 text-center">
                        {{ review.recommend ? 'Yes' : 'No' }}
                    </td>
                </tr>
            </tbody>
        </table>
    </section>
</template>

<script setup>
import { onMounted, watch, computed, ref } from 'vue';
import { useReviewsStore } from '@/stores/reviewsStore';

const store = useReviewsStore();

onMounted(async () => {
    await store.fetchAllReviews({ num: computedData.value });
    // console.log(store.users); // Check if the data is fetched successfully
    console.log(computedData.value)
});

const props = defineProps({
    fetchedNum: Number
})

let sortDirection = ref('');
let sortField = ref('')

const toggleSortDirection = async (value) => {
    if (sortDirection === 'ASC') {
        sortField = value;
        console.log(sortDirection);
        await sortBy(value, 'ASC');
        sortDirection = 'DESC';
    } else {
        sortField = value;
        console.log(sortDirection)
        await sortBy(value, 'DESC');
        sortDirection = 'ASC';
    }

}

const sortBy = async (value, direction = 'ASC') => {
    console.log(`tryingToSortBy: ${value}`)
    await store.fetchAllReviews({ order_by: value, order_direction: direction, num: computedData.value });
}

// Define a computed property to reactively access the data
const computedData = computed(() => props.fetchedNum);


// IMPORTANT
// Watch for changes to the parent variable
watch(() => props.fetchedNum, (newValue, oldValue) => {
    console.log('Parent variable changed:', oldValue, '=>', newValue);
    console.log(computedData.value);
    // You can perform any necessary actions here when the parent variable changes
});

</script>

<style lang="scss" scoped></style>