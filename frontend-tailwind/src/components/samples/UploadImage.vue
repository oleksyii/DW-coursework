<template>
    <div class="container mx-auto mt-8">
        <input type="file" @change="handleFileChange" accept="image/*" class="mb-4" />
        <div v-if="imagePreviewUrl" class="mb-4">
            <img :src="imagePreviewUrl" alt="Uploaded Image" class="max-w-xs max-h-xs mx-auto" />
        </div>
        <div v-if="byteArray" class="mb-4">
            <h2 class="text-lg font-semibold mb-2">Byte Array:</h2>
            <textarea class="w-full h-24 p-2 bg-gray-100 rounded" readonly v-model="byteArray"></textarea>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const imagePreviewUrl = ref('');
const byteArray = ref('');

const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = () => {
            imagePreviewUrl.value = reader.result;
            convertToByteArray(reader.result);
        };
        reader.readAsDataURL(file);
    }
};

const convertToByteArray = (dataUrl) => {
    const base64String = dataUrl.split(',')[1];
    const byteCharacters = atob(base64String);
    const byteArray = new Uint8Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
        byteArray[i] = byteCharacters.charCodeAt(i);
    }
    const byteString = byteArray.toString();
    console.log(byteString);
};
</script>

<style>
/* Add your custom styles here */
</style>
