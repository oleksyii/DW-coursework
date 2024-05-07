<template>
    <section>
        <div class="bg-blue-tag rounded-sm text-blue-cart hover:bg-blue-tag-bright hover:text-white">
            <p class=" px-1">{{ label }}</p>
        </div>
    </section>
</template>

<script setup>
import { computed, onMounted } from 'vue';

onMounted(() => {
    console.log(label.value)
})

const props = defineProps({
    label: {
        type: String,
        require: true
    }
})

const label = computed(() => props.label)

</script>

<style lang="scss" scoped></style>