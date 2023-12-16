<template>
  <div>
    <div>【Alert Level Distribution of Devices】</div>
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

const colors = ["rgb(124, 181, 236)", "rgb(53, 106, 196)", "rgb(22, 57, 122)"];
const levelValues = ["Low", "Medium", "High"].map((levelName) => props.data.map((item) => item.warningLevels.find((level) => level.name === levelName).value));
const renderChart = () => {
  const options = {
    legend: {
      data: ["Low", "Medium", "High"],
    },
    xAxis: [
      {
        type: "category",
        axisLine: {
          lineStyle: {
            color: "#22a2c3",
            opacity: 0.8,
          },
        },
        axisTick: {
          show: false,
        },
        axisLabel: {
          color: "#22a2c3",
        },
        data: ["Device A", "Device B", "Device C", "Device D", "Device E"],
      },
    ],
    yAxis: [
      {
        axisLine: {
          show: false,
        },
        axisTick: {
          show: false,
        },
        axisLabel: {
          color: "#22a2c3",
        },
        splitLine: {
          show: false, // 隐藏刻度线
        },
        type: "value",
      },
    ],
    grid: {
      containLabel: true,
    },
    itemStyle: {
      borderRadius: [5, 5, 0, 0],
    },
    series: levelValues.map((data, index) => ({
      name: data.device,
      type: "bar",
      barGap: 0,
      emphasis: {
        focus: "series",
      },
      data,
      itemStyle: {
        color: colors[index],
      },
    })),
  };

  myChart.setOption(options);
};

watch(() => props.data, renderChart);
</script>

<style scoped lang="scss"></style>
