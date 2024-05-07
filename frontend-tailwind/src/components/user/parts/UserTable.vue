<template>
    <section>
        <table class=" w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
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
                        <button class="uppercase" @click="toggleSortDirection('birth')">
                            <div class="flex">
                                Birth
                                <span v-if="sortField === 'birth'" class="ml-1">
                                    <span v-if="sortDirection === 'ASC'">▲</span>
                                    <span v-else>▼</span>
                                </span>
                            </div>
                        </button>
                    </th>
                    <th scope="col" class="text-center px-9 py-3">
                        <button class="uppercase" @click="toggleSortDirection('gender')">
                            <div class="flex">
                                Gender
                                <span v-if="sortField === 'gender'" class="ml-1">
                                    <span v-if="sortDirection === 'ASC'">▲</span>
                                    <span v-else>▼</span>
                                </span>
                            </div>
                        </button>
                    </th>
                    <th scope="col" class="text-center px-9 py-3">
                        <button class="uppercase" @click="toggleSortDirection('registration_date')">
                            <div class="flex">
                                Registration date
                                <span v-if="sortField === 'registration_date'" class="ml-1">
                                    <span v-if="sortDirection === 'ASC'">▲</span>
                                    <span v-else>▼</span>
                                </span>
                            </div>
                        </button>
                    </th>
                    <th scope="col" class="text-center px-9 py-3">
                        <button class="uppercase" @click="toggleSortDirection('country')">
                            <div class="flex">
                                Country
                                <span v-if="sortField === 'country'" class="ml-1">
                                    <span v-if="sortDirection === 'ASC'">▲</span>
                                    <span v-else>▼</span>
                                </span>
                            </div>
                        </button>
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Action
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(usr, index) in store.users" :key="index"
                    class="odd:bg-white odd:dark:bg-gray-900 even:bg-gray-50 even:dark:bg-gray-800 border-b dark:border-gray-700">
                    <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                        {{ usr.id }}
                    </th>
                    <td scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                        {{ usr.name }}
                    </td>
                    <td class=" py-4">
                        {{ usr.user_id_string }}
                    </td>
                    <td class="px-3 py-4">
                        {{ usr.birthDate }}
                    </td>
                    <td class="px-6 py-4 text-center">
                        {{ usr.gender }}
                    </td>
                    <td class="px-6 py-4">
                        {{ usr.registration_date }}
                    </td>
                    <td class="px-6 py-4">
                        {{ usr.country }}
                    </td>
                    <td class="px-6 py-4">
                        <a :href="usr.user_url"
                            class="font-medium text-blue-600 dark:text-blue-500 hover:underline">Show</a>
                    </td>
                </tr>
            </tbody>
        </table>
    </section>
</template>

<script setup>
import { onMounted, watch, computed, ref } from 'vue';
import { useUserStore } from '@/stores/usersStore.js';

const store = useUserStore();

onMounted(async () => {
    await store.fetchUserData({ num: computedData.value });
    console.log(store.users)
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
    await store.fetchUserData({ order_by: value, order_direction: direction, num: computedData.value });
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