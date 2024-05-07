<template>
    <div>
        <!-- Button to toggle the sidebar -->
        <button @click="toggleSidebar" class="fixed top-4 left-4 bg-blue-500 text-white px-3 py-1 rounded">Toggle
            Sidebar</button>

        <!-- Sidebar -->
        <Sidebar v-if="isSidebarOpen" @close="closeSidebar" />

        <!-- Page content -->
        <div @click="closeSidebar" class="ml-64 p-4">
            <h1 class="text-3xl font-bold">Main Content</h1>
            <p>Your main content goes here...</p>
        </div>
    </div>
</template>

<script setup>
import { useStore } from 'pinia';
import { defineComponent } from 'vue';
import Sidebar from './Sidebar.vue'; // Assuming Sidebar component file name

const store = useStore();

// Function to toggle sidebar state
const toggleSidebar = () => {
    store.toggleSidebar();
};

// Function to close sidebar
const closeSidebar = () => {
    store.closeSidebar();
};
</script>

<style scoped>
/* You can add custom styles for the sidebar and other elements here */
</style>
