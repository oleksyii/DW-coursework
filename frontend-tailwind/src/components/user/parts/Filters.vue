<!-- <template>
    <section>
        <form class="max-w-xs w-48 mr-2" @submit.prevent="submitForm" ref="form">
            <div class="mb-5">
                <label for="date" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                    Birth from</label>
                <input v-model="date" @input="validateDate" type="text" id="date" name="date"
                    class="mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm"
                    placeholder="YYYY-MM-DD" />
                <p v-if="!isValidDate" class="text-red-500 text-xs mt-1">
                    Please enter a valid date in the format YYYY-MM-DD and not a future date or earlier than 1900-01-01.
                </p>
            </div>
            <div class="mb-5">
                <label for="date" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                    Birth until</label>
                <input v-model="date" @input="validateDate" type="text" id="date" name="date"
                    class="mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm"
                    placeholder="YYYY-MM-DD" />
                <p v-if="!isValidDate" class="text-red-500 text-xs mt-1">
                    Please enter a valid date in the format YYYY-MM-DD and not a future date or earlier than 1900-01-01.
                </p>
            </div>
            <div class="mb-5">
                <label for="date" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                    Registration Date</label>
                <input v-model="registration_date" @input="validateDate" type="text" id="date" name="date"
                    class="mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm"
                    placeholder="YYYY-MM-DD" />
                <p v-if="!isValidDate" class="text-red-500 text-xs mt-1">
                    Please enter a valid date in the format YYYY-MM-DD and not a future date or earlier than 1900-01-01.
                </p>
            </div>
            <div class="mb-5">
                <label for="gender" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                    Gender</label>
                <select v-model="gender" id="gender" name="gender"
                    class="mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm">
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
                    class="mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm">
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

</script>

<style lang="scss" scoped>

</style> -->