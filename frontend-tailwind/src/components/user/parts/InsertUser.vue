<template>
    <section>
        <div class="mb-4">
            <span class="text-gray-900 text-2xl font-bold">Register a new user</span>
        </div>
        <form class="max-w-xs w-48 mr-2" @submit.prevent="submitForm" ref="form">
            <div class="mb-5">
                <label for="name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                    Name</label>
                <input v-model="name" type="text" id="name"
                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                    placeholder="Name" required />
            </div>
            <div class="mb-5">
                <label for="username" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                    Username</label>
                <input v-model="username" type="text" id="username"
                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                    placeholder="username" required />
            </div>
            <div class="mb-5">
                <label for="date" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                    Birth Date</label>
                <input v-model="date" @input="validateDate" type="text" id="date" nasame="date"
                    class="text-black mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm"
                    placeholder="YYYY-MM-DD" />
                <p v-if="!isValidDate" class="text-red-500 text-xs mt-1">
                    Please enter a valid date in the format YYYY-MM-DD and not a future date or earlier than 1900-01-01.
                </p>
            </div>
            <div class="mb-5 ">
                <label for="date" class="block mb-2 text-sm font-medium text-gray-900">
                    Registration Date</label>
                <input v-model="registration_date" @input="validateDate" type="text" id="date" name="date"
                    class="text-black mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm"
                    placeholder="YYYY-MM-DD" />
                <p v-if="!isValidDate" class="text-red-500 text-xs mt-1">
                    Please enter a valid date in the format YYYY-MM-DD and not a future date or earlier than 1900-01-01.
                </p>
            </div>
            <div class="mb-5">
                <label for="gender" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                    Gender</label>
                <select v-model="gender" id="gender" name="gender"
                    class="text-black mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm">
                    <option value="" disabled selected>Select gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                </select>
            </div>
            <div class="mb-5">
                <label for="country" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                    Choose the country</label>
                <select v-model="country" id="country" name="country"
                    class="text-black mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm">
                    <option value="" disabled selected>Select country</option>
                    <option v-for="(country, index) in fetchedData" :key="index" :value="country.country">{{
                        country.country }}</option>
                </select>
            </div>



            <div class="mb-5">
                <button :class="{ 'bg-gray-400 hover:bg-gray-400': !isFormValid }" type="submit"
                    :disabled="!isFormValid" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300
                font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600
                dark:hover:bg-blue-700 dark:focus:ring-blue-800">Submit</button>
            </div>
        </form>

    </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
// import { useCountryStore } from '@/stores/countryStore';

const name = ref('');
const username = ref('');
const date = ref('');
const isValidDate = ref(true);
const gender = ref('');
const country = ref('');
const registration_date = ref('');

// Define a ref to store the fetched data
const fetchedData = ref([]);

// Fetch data from the API when the component is mounted
onMounted(async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/countries');
        if (response.ok) {
            fetchedData.value = await response.json();
        } else {
            throw new Error('Failed to fetch data');
        }
    } catch (error) {
        console.error(error);
    }
});

const validateDate = () => {
    const regex = /^\d{4}-\d{2}-\d{2}$/;
    const currentDate = new Date();
    const inputDate = new Date(date.value);

    isValidDate.value = !!date.value.match(regex) &&
        inputDate <= currentDate &&
        inputDate >= new Date('1900-01-01');
};

// Computed property to determine if the form is valid
const isFormValid = computed(() => {
    return name.value !== '' &&
        username.value !== '' &&
        date.value !== '' &&
        isValidDate.value &&
        gender.value !== '' &&
        country.value !== '' &&
        registration_date.value !== '';
});

// Function to submit the form
const submitForm = async () => {
    const formData = {
        name: name.value,
        username: username.value,
        registration_date: registration_date.value,
        birthdate: date.value,
        gender: gender.value,
        country: country.value,
    };
    console.log(JSON.stringify(formData))

    const response = await fetch('http://127.0.0.1:8000/add-user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    });


    if (response.ok) {
        // Handle success
        console.log('Form submitted successfully');
        const data = await response.json()
        console.log(data.message);
    } else {
        // Handle error
        console.error('Failed to submit form:', response.statusText);
    }
};

</script>

<style lang="scss" scoped></style>