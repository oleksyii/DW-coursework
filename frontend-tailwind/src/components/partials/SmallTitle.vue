<template>

    <div class="flex items-center ml-48 bg-gray-800 text-white p-4 w-full fixed top-0 left-0 h-16">
        <h2 class="text-center text-3xl font-semibold w-full my-9 mr-48">
            {{ text }}
        </h2>

    </div>

</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
    text: {
        type: String,
        required: true
    }
});

const text = ref(props.text);
</script>

<style lang="scss" scoped></style>