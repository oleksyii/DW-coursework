    <template>
        <section >
            <table class=" max-w-5xl text-sm text-left rtl:text-right text-gray-400">
                <thead class="text-xs  uppercase bg-gray-700 text-gray-400">
                    <tr>
                        <th scope="col" class="px-6 py-3">
                            <button class="uppercase" @click="toggleSortDirection('id')">
                                Id
                                <span v-if="sortField === 'id'" class="ml-1">
                                    <span v-if="sortDirection === 'ASC'">▲</span>
                                    <span v-else>▼</span>
                                </span>
                            </button>
                        </th>
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
                            <button class="uppercase" @click="toggleSortDirection('status')">
                                <div class="flex">
                                    Status
                                    <span v-if="sortField === 'status'" class="ml-1">
                                        <span v-if="sortDirection === 'ASC'">▲</span>
                                        <span v-else>▼</span>
                                    </span>
                                </div>
                            </button>
                        </th>
                        <th scope="col" class="text-center px-9 py-3">
                            <button class="uppercase" @click="toggleSortDirection('order_date')">
                                <div class="flex">
                                    Order date
                                    <span v-if="sortField === 'order_date'" class="ml-1">
                                        <span v-if="sortDirection === 'ASC'">▲</span>
                                        <span v-else>▼</span>
                                    </span>
                                </div>
                            </button>
                        </th>
                        <th scope="col" class="text-center px-1 py-3">
                            <button class="uppercase" @click="toggleSortDirection('cancel_date')">
                                <div class="flex text-center">
                                    Cancellation date
                                    <span v-if="sortField === 'cancel_date'" class="ml-1">
                                        <span v-if="sortDirection === 'ASC'">▲</span>
                                        <span v-else>▼</span>
                                    </span>
                                </div>
                            </button>
                        </th>
                        <th scope="col" class="text-center px-9 py-3">
                            <button class="uppercase" @click="toggleSortDirection('games')">
                                <div class="flex">
                                    Game
                                    <span v-if="sortField === 'games'" class="ml-1">
                                        <span v-if="sortDirection === 'ASC'">▲</span>
                                        <span v-else>▼</span>
                                    </span>
                                </div>
                            </button>
                        </th>
                        <th scope="col" class="text-center px-9 py-3">
                            <button class="uppercase" @click="toggleSortDirection('sum')">
                                <div class="flex">
                                    Sum
                                    <span v-if="sortField === 'sum'" class="ml-1">
                                        <span v-if="sortDirection === 'ASC'">▲</span>
                                        <span v-else>▼</span>
                                    </span>
                                </div>
                            </button>
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(order, index) in store.orders" :key="index"
                        class="odd:bg-gray-900 even:bg-gray-800 border-b border-gray-700">
                        <th scope="row" class="px-6 py-4 font-medium whitespace-nowrap text-white">
                            {{ order.id }}
                        </th>
                        <td scope="row" class="px-6 py-4 font-medium whitespace-nowrap text-white">
                            {{ order.name }}
                        </td>
                        <td class=" py-4">
                            {{ order.username }}
                        </td>
                        <td class="px-2 py-4 text-center">
                            {{ order.status }}
                        </td>
                        <td class="px-2 py-4 text-center">
                            {{ order.order_date }}
                        </td>
                        <td class="px-2 py-4 text-center">
                            {{ order.cancel_date }}
                        </td>
                        <td class="px-6 py-4">
                            {{ order.games }}
                        </td>
                        <td class="px-6 py-4">
                            {{ order.sum }}$
                        </td>
                    </tr>
                </tbody>
            </table>
        </section>
    </template>

<script setup>
import { onMounted, watch, computed, ref } from 'vue';
import { useOrdersStore } from '@/stores/orderStore';

const store = useOrdersStore();

onMounted(async () => {
    await store.fetchOrderData({ num: computedData.value });
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
    await store.fetchOrderData({ order_by: value, order_direction: direction, num: computedData.value });
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