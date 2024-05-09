<template>
    <section>

        <button id="dropdownSearchButton" data-dropdown-toggle="dropdownSearch" data-dropdown-placement="bottom"
            class="text-white focus:ring-4 focus:outline-none font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center bg-blue-600 hover:bg-blue-700 focus:ring-blue-800"
            type="button">Filter countres <svg class="w-2.5 h-2.5 ms-3" aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="m1 1 4 4 4-4" />
            </svg>
        </button>

        <!-- Dropdown menu -->
        <div id="dropdownSearch" class="z-10 hidden rounded-lg shadow w-60 bg-gray-700">
            <div class="p-3">
            </div>
            <ul class="max-h-48 px-3 pb-3 overflow-y-auto text-sm text-gray-200" aria-labelledby="dropdownSearchButton">
                <li v-for="(country) in countries" :key="country.country_id">
                    <div class="flex items-center ps-2 rounded hover:bg-gray-600">
                        <input type="checkbox" :id="'checkbox-item-' + country.country_id" :value="country.country_id"
                            class="w-4 h-4 text-blue-600 rounded focus:ring-blue-600 ring-offset-gray-700 focus:ring-offset-gray-700 focus:ring-2 bg-gray-600 border-gray-500"
                            @change="toggleCheckbox(country.country_id)">
                        <label :for="'checkbox-item-' + country.country_id"
                            class="w-full py-2 ms-2 text-sm font-medium rounded text-gray-300">
                            {{ country.country }}
                        </label>
                    </div>
                </li>
            </ul>
            <button @click="fetchUsersWithFilters"
                class="flex items-center p-3 text-sm font-medium  border-t rounded-b-lg border-gray-600 bg-gray-700 hover:bg-gray-600 text-blue-cart hover:underline">
                <svg class="w-4 h-4 me-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor"
                    viewBox="0 0 20 18">
                    <path
                        d="M6.5 9a4.5 4.5 0 1 0 0-9 4.5 4.5 0 0 0 0 9ZM8 10H5a5.006 5.006 0 0 0-5 5v2a1 1 0 0 0 1 1h11a1 1 0 0 0 1-1v-2a5.006 5.006 0 0 0-5-5Zm11-3h-6a1 1 0 1 0 0 2h6a1 1 0 1 0 0-2Z" />
                </svg>
                Apply
            </button>
        </div>
    </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useUserStore } from '@/stores/usersStore';
import { initFlowbite } from 'flowbite';

const userStore = useUserStore()

const countries = ref([])
const checkedCheckboxes = ref({});

const toggleCheckbox = (countryId) => {
    if (checkedCheckboxes.value[countryId]) {
        delete checkedCheckboxes.value[countryId];
    } else {
        checkedCheckboxes.value[countryId] = true;
    }
    console.log(checkedCheckboxes.value)
}

// Fetch data from the API when the component is mounted
onMounted(async () => {
    initFlowbite();
    try {
        const response = await fetch('http://127.0.0.1:8000/countries');
        if (response.ok) {
            countries.value = await response.json();
        } else {
            throw new Error('Failed to fetch data');
        }
    } catch (error) {
        console.error(error);
    }
});

const fetchUsersWithFilters = () => {
    const selectedCountryIds = Object.keys(checkedCheckboxes.value);

    console.log(selectedCountryIds);

    userStore.fetchUserData({ "countries": selectedCountryIds })
}

</script>

<style lang="scss" scoped></style>