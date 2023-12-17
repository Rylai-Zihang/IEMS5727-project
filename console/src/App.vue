<template>
  <div class="bg-cover bg-center h-screen w-screen text-white overflow-hidden p-5 pt-0 flex flex-col" :style="{ backgroundImage: `url( ${currentBg} )` }">
    <h1 class="text-custom text-center p-3">Fire monitoring system</h1>
    <div class="flex flex-1" v-if="data">
      <div class="flex-1 mr-2 bg-opacity-50 bg-slate-800 p-3 flex flex-col">
        <StackBar class="h-1/2 box-border pb-4" :data="data.deviceWarningData" />
        <RadarChart class="h-1/2 box-border" :data="data.riskData" />
      </div>
      <div class="w-1/2 mr-2 flex flex-col opacity-80 bg-slate-800 p-3">
        <TotalData class="h-1/3" :data="data.aliveData" :total="data.totalData" />
        <Table class="h-2/3 opacity-80" :data="data.logData" />
      </div>
      <div class="flex-1 mr-2 flex flex-col opacity-50 bg-slate-800 p-3">
        <LineChart class="h-1/2" :data="data.temperatureData" />
      </div>
    </div>
    <div v-else class="bg-cover bg-center h-screen text-white p-2 flex overflow-hidden text-6xl justify-center items-center flex-row">
      <n-space class="flex flex-row">
        <span>Loading</span>
        <n-spin size="small" stroke="white" />
      </n-space>
    </div>
  </div>
</template>

<script setup>
import StackBar from "./components/StackBar.vue";
import RadarChart from "./components/RadarChart.vue";
import Table from "./components/Table.vue";
import TotalData from "./components/TotalData.vue";
import LineChart from "./components/LineChart.vue";
import { NSpin, NSpace } from "naive-ui";

import { provide, ref } from "vue";
import bg from "@/assets/img/bg.jpg";
import { getVisualization } from "./api/vis";

let currentBg = ref(bg);
provide("changeBackground", currentBg);

const data = ref(null);
const loadData = async () => {
  data.value = await getVisualization();
  console.log(JSON.stringify(data.value));
};

loadData();
// setInterval(() => {
loadData();
// }, 3000);
</script>

<style lang="scss" scoped></style>
