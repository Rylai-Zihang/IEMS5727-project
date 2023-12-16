<template>
  <div>
    <div>【Temperature Change Tendency】</div>
    <div ref="target" class="w-full h-full"></div>
  </div>
</template>

<script setup>
import * as echarts from "echarts";
import { ref, onMounted, watch, defineProps } from "vue";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

let myChart = null;
const target = ref(null);

onMounted(() => {
  myChart = echarts.init(target.value);
  renderChart();
});

const colors = ["#FCD34D", "#FFA500", "#FF7F50", "#FF6347", "#FF4500"];

const seriesData = props.data.map((t, index) => {
  return {
    name: t[0]?.["device"],
    type: "line",
    data: t.map((d, i) => {
      return d.temperature;
    }),
    smooth: true,
    color: colors[index],
  };
});

const timeData = props.data[0]?.map((item) => {
  return item["time"];
});

const renderChart = () => {
  const options = {
    xAxis: {
      type: "category",
      axisLabel: {
        color: "#fff",
      },
      data: timeData, // Assuming props.data.categories is an array of category labels
    },
    yAxis: {
      type: "value",
      axisLine: {
        show: false,
      },
      axisTick: {
        show: false,
      },
      splitLine: {
        show: false, // 隐藏刻度线
      },
      axisLabel: {
        color: "#fff",
      },
    },
    series: seriesData,
  };
  myChart.setOption(options);
};

watch(() => props.data, renderChart);
</script>

<style scoped lang="scss"></style>
