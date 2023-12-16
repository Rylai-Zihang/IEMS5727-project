<template>
  <div class="p-6">
    <div class="text-center text-slate-300">
      Total alert:
      <span ref="totalCountTarget" class="text-gradient font-[Electronic] text-7xl ml-2 mr-2 font-bold">{{ total }}</span>
      records
    </div>
    <div class="mt-3 flex flex-wrap">
      <div v-for="item in props.data" class="w-1/3 text-center text-slate-400 text-sm">
        <span class="font-[Electronic] text-slate-400 text-xl">{{ item["device"] + ":  " }}</span>
        <span :ref="item['device']" class="font-[Electronic] text-[#5dc5ef] text-3xl">{{ item["total_record"] }}</span>
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
