<template>
    <div id="tableViz">
        <div v-if="viz1">
            <tableau-viz id="tableauViz" src='https://public.tableau.com/views/OLAPV1backup/SalesV2' toolbar="bottom"
                hide-tabs>
            </tableau-viz>
        </div>
        <div v-if="!viz1">
            <tableau-viz id="tableauViz" src='https://public.tableau.com/views/OLAPV1backup/RatingsV2' toolbar="bottom"
                hide-tabs>
            </tableau-viz>
        </div>
        <button @click="toggleDashboard">Toggle Dashboard</button>
    </div>

</template>

<script setup>
import { ref } from "vue";
const viz1 = ref(false)

const toggleDashboard = () => {
    console.log(viz1.value)
    viz1.value = !viz1.value;
}

</script>

<style lang="scss" scoped></style>