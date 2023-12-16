<template>
  <div class="pt-3 pb-3">
    <div class="text-center text-slate-300">
      Total alert:
      <span ref="totalCountTarget" class="text-gradient text-7xl ml-2 mr-2 font-bold">{{ props.total }}</span>
      records
    </div>
    <div class="mt-3 flex flex-wrap">
      <div v-for="item in props.data" class="w-1/3 text-center text-slate-400 text-sm flex pb-3">
        <span class="text-slate-400 text-sm w-[100px]">{{ item["device"] + ":  " }}</span>
        <div>
          <n-tag v-if="item['camera_status']" type="success">camera online</n-tag>
          <n-tag v-else type="error">camera offline</n-tag>
          <div class="p-1"></div>
          <n-tag v-if="item['sensor_status']" type="success">sensor online</n-tag>
          <n-tag v-else type="error">sensor offline</n-tag>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, defineProps, watch } from "vue";

const totalCountTarget = ref(0);
const deviceA = ref(0);
const deviceB = ref(0);
const deviceC = ref(0);
const deviceD = ref(0);
const deviceE = ref(0);

const total = computed(() => {
  return deviceA.value + deviceB.value + deviceC.value + deviceD.value + deviceE.value;
});

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
  total: {
    type: Number,
    required: true,
  },
});

watch(
  () => props.data,
  (newValue) => {
    if (newValue.length >= 5) {
      deviceA.value = newValue[0].total_record;
      deviceB.value = newValue[1].total_record;
      deviceC.value = newValue[2].total_record;
      deviceD.value = newValue[3].total_record;
      deviceE.value = newValue[4].total_record;
    }
  }
);
</script>

<style scoped lang="scss"></style>
