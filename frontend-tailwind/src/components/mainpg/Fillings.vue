<template>
    <div class="absolute bottom-1 left-56 bg-my-gray rounded-sm shadow-md size-44 w-96 flex flex-col justify-center">
        <div class="relative mb-9 mx-2">
            <label data-tooltip-target="tooltip-default" for="labels-range-input"
                class=" text-gray-800 shadow-sm relative z-10">OLTP
                data to be
                filled</label>
            <div id="tooltip-default" role="tooltip"
                class="absolute z-30 invisible inline-block px-3 py-2 text-sm font-medium text-white bg-gray-800 rounded-lg shadow-sm opacity-0 tooltip dark:bg-gray-700">
                The num of users to be inserted.
                <div class="tooltip-arrow" data-popper-arrow></div>
            </div>
            <input id="labels-range-input" type="range" value="50" min="1" max="100"
                class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
                v-model="percent">
            <span class="text-sm text-gray-500 dark:text-gray-400 absolute start-0 -bottom-6">1%</span>
            <span
                class="text-sm text-gray-500 dark:text-gray-400 absolute start-1/2 -translate-x-1/2 rtl:translate-x-1/2 -bottom-6">50%</span>
            <span class="text-sm text-gray-500 dark:text-gray-400 absolute end-0 -bottom-6">100%</span>
        </div>
        <div class="flex items-center justify-center gap-4 ">
            <button @click="fillOLTP"
                class="w-28 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg">
                Fill OLTP
            </button>
            <button @click="fillOLAP"
                class="w-28 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg">
                FILL OLAP
            </button>
        </div>
    </div>
</template>

<script setup>
import { notifySuccess, notifyFail } from '@/utils/toast.js'
import { ref, onMounted } from 'vue';
import { initFlowbite } from 'flowbite'

// initialize components based on data attribute selectors
onMounted(() => {
    initFlowbite();
})


const percent = ref(50)

const showPercents = () => {
    console.log(percent.value);
}

const fillOLTP = async () => {
    const formData = {};
    console.log(JSON.stringify(formData))

    const response = await fetch(`http://127.0.0.1:8000/fill-oltp?percents=${percent.value}`, {
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
        notifySuccess(data.message)
    } else {
        // Handle error
        console.error('Failed to submit form:', response.statusText);
        notifyFail('Failed to submit form:', response.statusText)
    }
};

const fillOLAP = async () => {
    console.log(percent);
    const formData = {};
    console.log(JSON.stringify(formData))

    const response = await fetch('http://127.0.0.1:8000/fill-olap', {
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
        notifySuccess(data.message)
    } else {
        // Handle error
        console.error('Failed to submit form:', response.statusText);
        notifyFail('Failed to submit form:', response.statusText)
    }
};


</script>

<style lang="scss" scoped></style>