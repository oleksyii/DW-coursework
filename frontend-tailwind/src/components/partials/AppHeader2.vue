<template>
    <div>
        <nav class="bg-gray-900">
            <div class=" flex flex-wrap items-center mx-2 py-4 justify-between">
                <div class="flex gap-3">
                    <router-link :to="`/`" class="flex items-center space-x-3 rtl:space-x-reverse">
                        <!-- <img src="https://flowbite.com/docs/images/logo.svg" class="h-8" alt="Flowbite Logo" /> -->
                        <span class="self-center text-2xl font-semibold whitespace-nowrap text-white">GameStore</span>
                    </router-link>
                    <AppDrawer :links="navbarLinks" />
                    <CartModal />

                </div>
                <div class=" flex items-center md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse">
                    <button type="button"
                        class="flex text-sm bg-gray-800 rounded-full md:me-0 focus:ring-4 focus:ring-blue-cart"
                        id="user-menu-button" aria-expanded="false" data-dropdown-toggle="user-dropdown"
                        data-dropdown-placement="bottom">
                        <div class="flex items-center gap-2 p-3" id="navbar-user">
                            <span class="sr-only text-white">Open user menu</span>
                            <!-- <img class="w-8 h-8 rounded-full" src="/images/Profile.png" alt="user photo"> -->
                            <span class="text-gray-text text-md">{{ username }}</span>
                        </div>
                    </button>
                    <!-- Dropdown menu -->
                    <div class="z-50 hidden my-4 text-base list-none divide-y rounded-lg shadow bg-gray-700 divide-gray-600"
                        id="user-dropdown">
                        <div v-if="isSignedIn" id="navbar-user" class="px-4 py-3">
                            <span class="block text-sm text-white truncate">Your URL</span>
                            <a class="block text-sm  truncate text-gray-400 max-w-48 overflow-clip">link</a>
                        </div>
                        <ul class="py-2" aria-labelledby="user-menu-button">
                            <li v-if="isSignedIn">
                                <a href="#"
                                    class="block px-4 py-2 text-sm  hover:bg-gray-600 text-gray-200 hover:text-white">Sign
                                    Out</a>
                            </li>
                            <li v-else>
                                <a href="#"
                                    class="block px-4 py-2 text-sm  hover:bg-gray-600 text-gray-200 hover:text-white">Sign
                                    In</a>
                            </li>
                        </ul>
                    </div>
                    <button data-collapse-toggle="navbar-user" type="button"
                        class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm rounded-lg md:hidden focus:outline-none focus:ring-2 text-gray-400 hover:bg-gray-700 focus:ring-gray-600"
                        aria-controls="navbar-user" aria-expanded="false">
                        <span class="sr-only">Open main menu</span>
                        <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                            viewBox="0 0 17 14">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M1 1h15M1 7h15M1 13h15" />
                        </svg>
                    </button>
                </div>
                <!-- <div class="items-center justify-between hidden w-full md:flex md:w-auto md:order-1" id="navbar-user">
                    <ul
                        class="flex flex-col font-medium p-4 md:p-0 mt-4 border rounded-lg md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0 md:border-0 bg-gray-800 md:bg-gray-900 border-gray-700">

                        <li v-for="(elem, index) in headerLinks" :key="index">
                            <a :href="elem.url"
                                class="block py-2 px-3 rounded  md:p-0 text-gray-text md:hover:text-blue-500 hover:bg-gray-700 hover:text-white md:hover:bg-transparent border-gray-700 text-lg font-semibold"
                                aria-current="page">{{ elem.label }}</a>
                        </li>

                    </ul>
                </div> -->
            </div>
        </nav>

    </div>
</template>

<script setup>
import { useRegistrationStore } from "@/stores/registrationStore";
import { useGamesStore } from "@/stores/gamesStore";
import { ref, onMounted } from "vue";
import AppDrawer from "./AppDrawer.vue";
import CartModal from "../mainpg/CartModal.vue";
import { initFlowbite } from 'flowbite'

const registrationStore = useRegistrationStore();
const gamesStore = useGamesStore()

// const username = ref(registrationStore.activeUser);
const username = ref(gamesStore.activeUser)
const isSignedIn = ref(gamesStore.isSignedIn);
const isAdmin = ref(gamesStore.isAdmin);

// const headerLinks = ref([
//     { label: 'Волонтеру', url: '/' },
//     { label: 'Шукачу', url: '/' },
// ]);

onMounted(() => {
    initFlowbite();
})

const navbarLinks = ref([
    { label: 'Main', url: '/', imgUrl: '/question.png' },
    { label: 'User', url: '/users', imgUrl: '/question.png' },
    { label: 'Order', url: '/orders', imgUrl: '/question.png' },
    { label: 'Review', url: '/reviews', imgUrl: '/question.png' },
    { label: 'Export', url: '/export', imgUrl: '/question.png' },
    { label: 'BI', url: '/bi', imgUrl: '/question.png' },
]);

</script>

<style lang="scss" scoped></style>