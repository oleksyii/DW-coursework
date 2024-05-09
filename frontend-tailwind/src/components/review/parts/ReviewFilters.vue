<template>
    <section class="flex justify-center gap-2 items-center">
        <div class="max-w-48 relative">

            <input v-model="date_from" @input="validateDateFrom" type="text" id="date_from" name="dateFrom"
                class="text-black border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm"
                placeholder="Date from (YYYY-MM-DD)" />
            <p v-if="!isValidDateFrom" class="text-red-500 text-xs mt-1 text-nowrap absolute">
                Please enter a valid date in the format YYYY-MM-DD and not a future date or earlier than 1900-01-01.
            </p>
        </div>
        <div class="max-w-48 relative">
            <input v-model="date_to" @input="validateDateTo" type="text" id="date_to" name="dateTo"
                class="text-black border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm"
                placeholder="Date to (YYYY-MM-DD)" />
            <p v-if="!isValidDateTo" class="text-red-500 text-xs mt-1 text-nowrap absolute">
                Please enter a valid date in the format YYYY-MM-DD and not a future date or earlier than 1900-01-01.
            </p>
        </div>

        <div class="w-96 relative">
            <input v-model="game_name" type="text" id="game_name" name="date"
                class="text-black border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm"
                placeholder="Game" />
        </div>

        <div class="flex items-center mb-4">
            <input id="default-checkbox" type="checkbox" value="" v-model="is_only_interacted"
                class="w-4 h-4 text-blue-600 rounded focus:ring-blue-600 ring-offset-gray-800 focus:ring-2 bg-blue-cart border-gray-600">
            <label for="default-checkbox" class="ms-2 text-sm font-medium text-gray-300">Only interacted reviews</label>
        </div>





        <!-- Apply -->
        <button @click="fecthReviewsWithFilters"
            class="flex items-center p-3 text-sm font-medium  border-t rounded-b-lg border-gray-600 bg-gray-700 hover:bg-gray-600 text-blue-cart hover:underline">
            <svg class="w-4 h-4 me-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor"
                viewBox="0 0 20 18">
                <path
                    d="M6.5 9a4.5 4.5 0 1 0 0-9 4.5 4.5 0 0 0 0 9ZM8 10H5a5.006 5.006 0 0 0-5 5v2a1 1 0 0 0 1 1h11a1 1 0 0 0 1-1v-2a5.006 5.006 0 0 0-5-5Zm11-3h-6a1 1 0 1 0 0 2h6a1 1 0 1 0 0-2Z" />
            </svg>
            Apply
        </button>

    </section>
</template>

<script setup>
import { useReviewsStore } from '@/stores/reviewsStore';
import { initFlowbite } from 'flowbite';
import { onMounted, ref, watch, computed } from 'vue'

const store = useReviewsStore();

const isValidDateTo = ref(true);
const isValidDateFrom = ref(true);
const date_from = ref('')
const date_to = ref('')
const game_name = ref('')
const is_only_interacted = ref(false)

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

const fecthReviewsWithFilters = () => {
    let filters = { "game_name": null, "date_from": null, "date_to": null, "is_only_interacted": null }
    console.log(is_only_interacted.value)
    if (game_name.value.length > 0) {
        filters["game_name"] = game_name.value;
    }
    if (date_from.value.length > 0) {
        filters["date_from"] = date_from.value;
    }
    if (date_to.value.length > 0) {
        filters["date_to"] = date_to.value;
    }
    if (is_only_interacted.value) {
        filters["is_only_interacted"] = is_only_interacted.value;
    }


    console.log(filters);

    store.fetchAllReviews(filters)
}

</script>

<style lang="scss" scoped></style>