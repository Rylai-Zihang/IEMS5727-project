<template>
  <div>
    <div>【Camera Alert Level Distribution of Devices】</div>
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
const levels = ["Low", "Medium", "High"];
const levelValues = levels.map((levelName) => props.data.map((item) => item.warningLevels.find((level) => level.name === levelName).value));
const renderChart = () => {
  const deviceNames = props.data.map((item) => item.device); // 获取设备名称
  const seriesData = props.data.map((item) => item.warningLevels.map((level) => level.value)); // 获取警报级别数据
  const options = {
    legend: {
      data: levels,
    },
    tooltip: {
      trigger: "item",
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
        data: deviceNames,
      },
    ],
    yAxis: [
      {
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
        splitLine: {
          show: false, // 隐藏刻度线
        },
        type: "value",
      },
    ],
    grid: {
      left: "3%",
      right: "3%",
      top: "10%",
      bottom: "10%",
      containLabel: true,
    },
    itemStyle: {
      borderRadius: [5, 5, 0, 0],
    },
    series: levels.map((level, index) => ({
      name: level,
      type: "bar",
      barGap: 0,
      emphasis: {
        focus: "series",
      },
      data: seriesData.map((data) => data[index]),
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
