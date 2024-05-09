<template>
    <section class="flex justify-center gap-2 items-center">


        <div class="max-w-48 relative">

            <input v-model="date_from" @input="validateDateFrom" type="text" id="date" name="date"
                class="text-black border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm"
                placeholder="Date from (YYYY-MM-DD)" />
            <p v-if="!isValidDateFrom" class="text-red-500 text-xs mt-1 text-nowrap absolute">
                Please enter a valid date in the format YYYY-MM-DD and not a future date or earlier than 1900-01-01.
            </p>
        </div>
        <div class="max-w-48 relative">
            <input v-model="date_to" @input="validateDateTo" type="text" id="date" name="date"
                class="text-black border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm"
                placeholder="Date to (YYYY-MM-DD)" />
            <p v-if="!isValidDateTo" class="text-red-500 text-xs mt-1 text-nowrap absolute">
                Please enter a valid date in the format YYYY-MM-DD and not a future date or earlier than 1900-01-01.
            </p>
        </div>

        <!-- Dropdown menu -->
        <div>
            <button id="dropdownSearchButton" data-dropdown-toggle="dropdownSearch" data-dropdown-placement="bottom"
                class="text-white focus:ring-4 focus:outline-none font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center bg-blue-600 hover:bg-blue-700 focus:ring-blue-800"
                type="button">Filter status <svg class="w-2.5 h-2.5 ms-3" aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="m1 1 4 4 4-4" />
                </svg>
            </button>


            <div id="dropdownSearch" class="z-10 hidden rounded-lg shadow w-60 bg-gray-700">
                <ul class=" max-h-48 px-3 py-2 overflow-y-auto text-sm text-gray-200"
                    aria-labelledby="dropdownSearchButton">
                    <li v-for="(status, index) in statuses" :key="index">
                        <div class="flex items-center ps-2 rounded hover:bg-gray-600">
                            <input type="checkbox" :id="'checkbox-item-' + status.country_id" :value="status.country_id"
                                class="w-4 h-4 text-blue-600 rounded focus:ring-blue-600 ring-offset-gray-700 focus:ring-offset-gray-700 focus:ring-2 bg-gray-600 border-gray-500"
                                @change="toggleCheckbox(status)">
                            <label :for="'checkbox-item-' + status"
                                class="w-full py-2 ms-2 text-sm font-medium rounded text-gray-300">
                                {{ status }}
                            </label>
                        </div>
                    </li>
                </ul>
                <button @click="fetchOrdersWithFilters"
                    class="flex items-center p-3 text-sm font-medium  border-t rounded-b-lg border-gray-600 bg-gray-700 hover:bg-gray-600 text-blue-cart hover:underline">
                    <svg class="w-4 h-4 me-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor"
                        viewBox="0 0 20 18">
                        <path
                            d="M6.5 9a4.5 4.5 0 1 0 0-9 4.5 4.5 0 0 0 0 9ZM8 10H5a5.006 5.006 0 0 0-5 5v2a1 1 0 0 0 1 1h11a1 1 0 0 0 1-1v-2a5.006 5.006 0 0 0-5-5Zm11-3h-6a1 1 0 1 0 0 2h6a1 1 0 1 0 0-2Z" />
                    </svg>
                    Apply
                </button>
            </div>
        </div>

    </section>
</template>

<script setup>
import { useOrdersStore } from '@/stores/orderStore';
import { initFlowbite } from 'flowbite';
import { onMounted, ref, watch, computed } from 'vue'

const store = useOrdersStore();

const isValidDateTo = ref(true);
const isValidDateFrom = ref(true);
const date_from = ref('')
const date_to = ref('')
const statuses = ref([
    "Completed",
    "Pending",
    "Cancelled",
])

const checkedCheckboxes = ref({});

onMounted(async () => {
    initFlowbite()
})

const toggleCheckbox = (status) => {
    if (checkedCheckboxes.value[status]) {
        delete checkedCheckboxes.value[status];
    } else {
        checkedCheckboxes.value[status] = true;
    }
    console.log(checkedCheckboxes.value)
}

const applyFilters = () => {
    console.log(date_from.value);
}

const validateDateFrom = () => {
    const regex = /^\d{4}-\d{2}-\d{2}$/;
    const currentDate = new Date();
    const inputDate = new Date(date_from.value);

    isValidDateFrom.value = !!date_from.value.match(regex) &&
        inputDate <= currentDate &&
        inputDate >= new Date('1900-01-01');
};

const validateDateTo = () => {
    const regex = /^\d{4}-\d{2}-\d{2}$/;
    const currentDate = new Date();
    const inputDate = new Date(date_to.value);

    isValidDateTo.value = !!date_to.value.match(regex) &&
        inputDate <= currentDate &&
        inputDate >= new Date('1900-01-01') &&
        inputDate >= new Date(date_from.value);
};
// Computed property to determine if the form is valid
const isFormValid = computed(() => {
    return
});

const fetchOrdersWithFilters = () => {
    const selectedStatuses = Object.keys(checkedCheckboxes.value);
    let filters = { "status": null, "date_from": null, "date_to": null }
    console.log(date_from.value)
    if (selectedStatuses.length > 0) {
        filters["status"] = selectedStatuses;
    }
    if (date_from.value.length > 0) {
        filters["date_from"] = date_from.value;
    }
    if (date_to.value.length > 0) {
        filters["date_to"] = date_to.value;
    }


    console.log(filters);

    store.fetchOrderData(filters)
}

</script>

<style lang="scss" scoped></style>