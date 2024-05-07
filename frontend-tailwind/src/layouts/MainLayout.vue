<template>
    <div>
        <!-- <AppHeader /> -->
        <AppHeader2 />
        <main>
            <router-view />
        </main>
        <AppSidebar />
    </div>
</template>

<script setup>
import AppHeader from '@/components/partials/AppHeader.vue';
import AppSidebar from '@/components/partials/AppSidebar.vue';
import AppHeader2 from '@/components/partials/AppHeader2.vue';
</script>

<style lang="scss" scoped></style>