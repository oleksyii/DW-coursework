<template>
    <component :is="layout">
        <RouterView />
    </component>
</template>


<script setup>
import { RouterView, useRoute } from 'vue-router';
import MainLayout from '@/layouts/MainLayout.vue';
import { watch, shallowRef } from 'vue';

const layout = shallowRef(null);
const route = useRoute();

watch(
    () => route.meta,
    async (meta) => {
        try {
            const component = await import(`@/layouts/${meta?.layout}.vue`);
            layout.value = component?.default || MainLayout;
        } catch (e) {
            layout.value = MainLayout;
        }
    }
);

</script>