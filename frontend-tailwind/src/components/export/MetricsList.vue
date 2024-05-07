<template>
    <div>
        <!-- <ul class="divide-y divide-gray-300 bg-slate-800 max-w-sm mt-16 mx-auto px-4 border">

            <li class="py-4">

                <div class="flex items-center space-x-4">
                    <span class="text-lg font-bold">Item 1</span>
                </div>

                <ul class="divide-y divide-gray-300 bg-inherit rounded-md px-4 py-2 mt-4">
                    <li class="py-2">
                        <div class="flex flex-col space-x-4">
                            <label v-for="(value, name) in checkboxNames" :key="name">
                                <input type="checkbox" :value="value" v-model="checkboxDict[name]"
                                    @change="updateCheckbox(name)">
                                {{ name }}
                            </label>
                        </div>
                        <div class="flex items-center space-x-4">
                            <span class="text-md font-medium">Subitem 1</span>
                        </div>
                    </li>

                    <li class="py-2">
                        <div class="flex items-center space-x-4">
                            <span class="text-md font-medium">Subitem 2</span>
                        </div>

                        <ul class="divide-y divide-gray-300 bg-inherit rounded-md px-4 py-2 mt-2">
                            <li class="py-2">
                                <div class="flex items-center space-x-4">
                                    <span class="text-sm font-medium">Sub-subitem 1</span>
                                </div>
                            </li>
                            <li class="py-2">
                                <div class="flex items-center space-x-4">
                                    <span class="text-sm font-medium">Sub-subitem 2</span>
                                </div>
                            </li>
                        </ul>
                    </li>

                    <li class="py-2">
                        <div class="flex items-center space-x-4">
                            <span class="text-md font-medium">Subitem 3</span>
                        </div>
                    </li>
                </ul>

            </li>

        </ul> -->

        <div class="bg-gray-800 p-4 rounded-lg">
            <select v-model="selectedFact" class="text-white bg-gray-800 rounded-md p-2">
                <option v-for="(fact, index) in store.metadata.facts" :key="index" :value="fact.name">{{ fact.name }}
                </option>
            </select>
            <div v-if="selectedFact" class="mt-4">
                <h2 class="text-xl text-white">{{ selectedFact }}</h2>
                <h3 class="text-lg text-white mt-2">Dimensions</h3>
                <div v-for="(dimension, index) in getDimensions(selectedFact)" :key="index" class="ml-4 mt-2">
                    <label class="flex items-center text-white">
                        <input type="checkbox" :value="dimension.name" v-model="selectedDimensions" class="mr-2">
                        {{ dimension.name }}
                    </label>
                    <div v-if="dimension.hierarchies && dimension.hierarchies.length" class="ml-4">
                        <div v-for="(hierarchy, hierarchyIndex) in dimension.hierarchies" :key="hierarchyIndex"
                            class="ml-2 mt-1">
                            <label class="flex items-center text-white">
                                <input type="checkbox" :value="hierarchy" v-model="selectedHierarchies" class="mr-2">
                                {{ hierarchy }}
                            </label>
                        </div>
                    </div>
                </div>
                <h3 class="text-lg text-white mt-4">Metrics</h3>
                <div v-for="(metric, index) in getMetrics(selectedFact)" :key="index" class="ml-4 mt-2">
                    <label class="flex items-center text-white">
                        <input type="checkbox" :value="metric.name" v-model="selectedMetrics" class="mr-2">
                        {{ metric.name }}
                    </label>
                </div>
            </div>
        </div>
        <button @click="exportData" class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Export Data
        </button>
    </div>
</template>

<script setup>
import { useMetadataStore } from '@/stores/metadataStore';
import { onMounted, ref, computed } from 'vue';
import { notifySuccess, notifyFail } from '@/utils/toast.js'

const store = useMetadataStore();


onMounted(async () => {
    await store.fetchMetadata();
    console.log(store.metadata.facts[0]);
    store.metadata.facts.forEach(fact => {
        console.log(fact.name);
    })
    console.log('Dummy');
    // facts = store.metadata.facts;
    console.log(getMetrics('Sales')[0].name);
});

const selectedFact = ref(null);
const selectedDimensions = ref([]);
const selectedHierarchies = ref([]);
const selectedMetrics = ref([]);

const getDimensions = (factName) => {
    const fact = store.metadata.facts.find(fact => fact.name === factName);
    return fact ? fact.dimensions : [];
};

const getMetrics = (factName) => {
    const fact = store.metadata.facts.find(fact => fact.name === factName);
    return fact ? fact.metrics : [];
};

const exportData = () => {
    let fact = selectedFact.value;
    let dimensions = selectedDimensions.value;
    let tempDims = []
    tempDims.push(...selectedDimensions.value)
    tempDims.push(...selectedHierarchies.value)
    // dimensions.push(...selectedHierarchies.value);
    let hierarchies = selectedHierarchies.value;
    let metrics = selectedMetrics.value;

    console.log(tempDims)
    console.log(fact, dimensions, hierarchies, metrics);

    // Prepare the data object to send to the endpoint
    const dataToSend = {
        fact: fact,
        dimensions: tempDims,
        metrics: metrics
    };

    // Configure the fetch request
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    };

    console.log(requestOptions);

    // Send the fetch request to the endpoint
    fetch('http://127.0.0.1:8000/export', requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to export data');
            }
            return response.json();
        })
        .then(data => {
            console.log('Data exported successfully:', data);
            notifySuccess('Data exported successfully');
        })
        .catch(error => {
            console.error('Error exporting data:', error);
            notifyFail('Error exporting data')
        });


};


// const getDimensions = (factName) => {
//     const fact = facts.find(fact => fact.name === factName);
//     return fact ? fact.dimensions : [];
// };

// const getMetrics = (factName) => {
//     const fact = facts.find(fact => fact.name === factName);
//     return fact ? fact.metrics : [];
// };

// // Initialize checkedDimensions and checkedHierarchies with empty objects for each fact
// facts.forEach(fact => {
//     checkedDimensions.value[fact.name] = [];
//     checkedHierarchies.value[fact.name] = {};
// });

// // Watch for changes in selectedFact and reset checkedDimensions and checkedMetrics accordingly
// const selectedFactWatcher = computed(() => {
//     const dimensions = getDimensions(selectedFact.value);
//     const metrics = getMetrics(selectedFact.value);
//     const initialCheckedDimensions = {};
//     const initialCheckedMetrics = {};
//     dimensions.forEach(dimension => {
//         initialCheckedDimensions[dimension.name] = [];
//         if (dimension.hierarchies && dimension.hierarchies.length) {
//             dimension.hierarchies.forEach(hierarchy => {
//                 initialCheckedHierarchies[hierarchy] = false;
//             })
//         }
//     });
//     metrics.forEach(metric => {
//         initialCheckedMetrics[metric.name] = [];
//     });
//     checkedDimensions.value = initialCheckedDimensions;
//     checkedHierarchies.value = initialCheckedHierarchies;
//     checkedMetrics.value = initialCheckedMetrics;
//     console.log(checkedHierarchies)
// });



// // Exporting Data
// const exportData = () => {
//     const fact = selectedFact.value;
//     const dimensions = checkedDimensions.value[fact];
//     const metrics = checkedMetrics.value[fact];


//     console.log(checkedHierarchies.value);


// };


</script>

<style lang="scss" scoped></style>