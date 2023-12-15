<template>
  <div class="bg-cover bg-center h-screen w-screen text-white p-2 flex overflow-hidden" v-if="data" :style="{ backgroundImage: `url( ${currentBg} )` }">
    <div class="flex-1 mr-2 bg-opacity-50 bg-slate-800 p-3 flex flex-col">
      <StackBar class="h-1/2 box-border pb-4" :data="data.deviceData" />
      <RadarChart class="h-1/2 box-border pb-4" :data="data.riskData" />
    </div>
    <div class="w-2/3 mr-2 flex flex-col">
      <!-- <TotalData class="opacity-50 bg-slate-800 p-3" :data="data.totalData" /> -->
      <!-- <EventChart class="opacity-50 bg-slate-800 p-3 mt-2 flex-1" :data="data.mapData" /> -->
    </div>
  </div>
  <div v-else :style="{ backgroundImage: `url( ${currentBg} )` }" class="bg-cover bg-center h-screen text-white p-2 flex overflow-hidden text-6xl justify-center items-center flex-row">
    <n-space class="flex flex-row">
      <span>加载中请稍后</span>
      <n-spin size="small" stroke="white" />
      <n-spin size="small" stroke="white" />
      <n-spin size="small" stroke="white" />
    </n-space>
  </div>
</template>

<script setup>
import StackBar from "./components/StackBar.vue";
import HeatMap from "./components/HeatMap.vue";
import RadarChart from "./components/RadarChart.vue";
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
setInterval(() => {
  loadData();
}, 3000);
</script>

<style lang="scss" scoped></style>
