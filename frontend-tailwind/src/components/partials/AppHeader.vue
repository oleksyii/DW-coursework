<template>
  <section class="flex justify-end">
    <header class="w-full h-20 px-4 py-2 flex items-center justify-between shadow-md bg-gray-800">
      <AppDrawer :links="navbarLinks" />
      <CartModal />
      <div
        class="absolute mt-[620px] md:mt-48 z-50 bg-gray-800 w-[157px] h-contain md:flex justify-center shadow-sm right-0"
        v-if="isProfileOpen">
        <div class="flex flex-col text-2xl text-center text-dark-text">
          <router-link :to="profileUrl" class="py-6">
            <span class="text-3xl font-semibold">Profile</span>
          </router-link>
          <div class="bottom-0 pb-3 text-center">
            <button @click="handleSignOut">
              <span class="border-t-2 text-red-700 font-semibold">Logout</span>
            </button>
          </div>
        </div>
      </div>
      <ul class="hidden md:flex flex-1 justify-center gap-x-10">
        <li v-for="(item, idx) in headerLinks" :key="idx" class="text-dark-text text-lg hover:underline">
          <router-link :to="item.url">
            {{ item.label }}
          </router-link>
        </li>
      </ul>
      <div>
        <div :class="isLoggedIn ? 'hidden' : 'md:flex hidden justify-center items-center gap-x-6'">
          <button class="px-3 py-2" @click="openLoginPopup">
            <span class="font-semibold hover:underline">Вхід</span>
          </button>
          <button @click="openRegisterPopup">
            <span class="font-semibold hover:underline">Реєстрація</span>
          </button>
        </div>
        <div :class="isLoggedIn ? 'hidden md:flex flex-row items-center gap-x-4' : 'hidden'">
          <div class="flex flex-col items-center">
            <span class="font-bold text-white bg-primary p-1 text-center">{{ profileData.full_name }}
            </span>
          </div>
          <button @click="openProfileDropdown">
            <img class="w-14" src="/images/Profile.png" alt="" />
          </button>
        </div>

        <BurgerIcon @click="toggleDropdown" class="object-contain w-10 md:hidden" />

        <div v-if="isDropdownOpen" class="flex flex-col">
          <ul class="absolute z-10 w-full flex flex-col items-start top-20 right-0 bg-gray-800 shadow-md md:hidden">
            <li v-for="(item, idx) in headerLinks" :key="idx"
              class="text-dark-text text-xl w-full h-full px-4 py-2 hover:bg-primary">
              <router-link :to="item.url">
                {{ item.label }}
              </router-link>
            </li>
            <div :class="isLoggedIn ? 'hidden' : 'p-4 flex justify-end w-full'">
              <button class="px-3 py-2" @click="openLoginPopup">
                <span class="font-semibold hover:underline">Вхід</span>
              </button>
              <button @click="openRegisterPopup">
                <span class="font-semibold hover:underline">Реєстрація</span>
              </button>
            </div>
            <div :class="isLoggedIn ? 'w-full flex items-center justify-end text-center px-6 py-4' : 'hidden'
              ">
              <span class="font-bold text-white bg-primary p-2 text-center">{{ profileData.full_name }}
              </span>
              <button @click="openProfileDropdown">
                <img class="w-11 md:w-14" src="/images/Profile.png" alt="" />
              </button>
            </div>
          </ul>
        </div>
      </div>
    </header>

  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
import { useSidebarStore } from '@/stores/sidebarStore';
import ListItem from '@/components/utils/ListItem.vue';
import BurgerIcon from '@/components/icons/BurgerIcon.vue'
import { initFlowbite } from 'flowbite'
import CartModal from '@/components/mainpg/CartModal.vue';
import AppDrawer from '@/components/partials/AppDrawer.vue'
import { useRegistrationStore } from '@/stores/registrationStore';
// import BurgerIconVue from '../icons/BurgerIcon.vue';
const authStore = useAuthStore();
const sidebarStore = useSidebarStore();
const registrationStore = useRegistrationStore();

const isLoggedIn = computed(() => authStore.isLoggedIn);
const profileData = computed(() => authStore.profileData);

const isSidebarOpen = computed(() => sidebarStore.isSidebarOpen);


const router = useRouter();

onMounted(() => {
  initFlowbite();
})

function handleSignOut() {
  registrationStore.deactivateUser();
  authStore.signOut();
  router.push('/');
}

const requestUrl = '/my-requests';
const applyUrl = '/my-applies';
const profileUrl = '/me';

const headerLinks = ref([
  { label: 'Волонтеру', url: '/' },
  { label: 'Шукачу', url: '/' },
]);

const navbarLinks = ref([
  { label: 'Main', url: '/', imgUrl: '/question.png' },
  { label: 'User', url: '/users', imgUrl: '/question.png' },
  { label: 'Order', url: '/', imgUrl: '/question.png' },
  { label: 'Review', url: '/', imgUrl: '/question.png' },
  { label: 'Export', url: '/export', imgUrl: '/question.png' },
  { label: 'BI', url: '/bi', imgUrl: '/question.png' },
]);

const isDropdownOpen = ref(false);
const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
};
const isProfileOpen = ref(false);

const openProfileDropdown = () => {
  isProfileOpen.value = !isProfileOpen.value;
};

function openRegisterPopup() {
  authStore.setRegisterPopupOpenStatus(true);
}
function openLoginPopup() {
  authStore.setLoginPopupOpenStatus(true);
}


const toggleSidebar = useSidebarStore().toggleSidebar;

</script>
