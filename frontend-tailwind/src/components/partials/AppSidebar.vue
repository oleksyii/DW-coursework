<template>
    <transition name="sidebar-transition">
        <div ref="sidebar" :class="{ 'hidden': !isSidebarOpen, 'sidebar': isSidebarOpen }"
            class="transition-transform duration-300 ease-in-out transform">

            <aside id="default-sidebar"
                class="fixed top-0 left-0 z-40 w-48 h-screen transition-transform -translate-x-full sm:translate-x-0"
                aria-label="Sidebar">
                <div class="h-full px-3 py-4 overflow-y-auto bg-gray-50 dark:bg-gray-800">
                    <div class="flex justify-end h-4">
                        <button @click="toggleSidebar">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round"
                                stroke-linejoin="round">
                                <line x1="18" y1="6" x2="6" y2="18"></line>
                                <line x1="6" y1="6" x2="18" y2="18"></line>
                            </svg>
                        </button>
                    </div>
                    <ul class="space-y-5 font-medium">
                        <li v-for="(link, index) in navbarLinks" :key="index" class="border-b">
                            <router-link :to="link.url"
                                class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group">
                                <img :src="link.imgUrl" alt="Description of the image"
                                    class="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" />
                                <span class="flex-1 ms-3 whitespace-nowrap">{{ link.label }}</span>
                            </router-link>
                        </li>
                    </ul>
                </div>
            </aside>
        </div>
    </transition>
</template>


<script setup>
import { ref, computed } from 'vue';
import { useSidebarStore } from '@/stores/sidebarStore';

const isSidebarOpen = computed(() => useSidebarStore().isSidebarOpen);
const toggleSidebar = useSidebarStore().toggleSidebar;

// TODO: replace with actual links
const navbarLinks = ref([
    { label: 'Main', url: '/', imgUrl: '/question.png' },
    { label: 'User', url: '/users', imgUrl: '/question.png' },
    { label: 'Order', url: '/', imgUrl: '/question.png' },
    { label: 'Review', url: '/', imgUrl: '/question.png' },
    { label: 'Export', url: '/export', imgUrl: '/question.png' },
    { label: 'BI', url: '/bi', imgUrl: '/question.png' },
]);
</script>

<style lang="scss" scoped></style>