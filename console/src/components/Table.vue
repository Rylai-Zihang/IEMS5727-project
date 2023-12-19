<template>
  <div>
    <div class="pt-5 pb-3">【Alert Log Table】</div>
    <div class="max-h-[390px] overflow-y-auto overflow-x-hidden">
      <n-data-table :columns="columns" :data="data" :pagination="pagination" :bordered="false" />
    </div>
  </div>
</template>

<script>
import { h, defineComponent, defineProps, ref } from "vue";
import { NImage } from "naive-ui";

const createColumns = ({ showShortcut }) => [
  {
    title: "Device",
    key: "device",
  },
  {
    title: "Time",
    key: "time",
  },
  {
    title: "Alert Level",
    key: "level",
  },
  {
    title: "Dealt",
    key: "dealt",
  },
  {
    title: "Shortcut",
    key: "shortcut",
    render(row) {
      return h(NImage, {
        width: 50,
        src: row.shortcut,
        previewedImgProps: {
          style: {
            width: 200,
            border: "8px solid white",
          },
        },
      });
    },
  },
];

export default defineComponent({
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const pagination = ref({
      page: 1, // 当前页码
      pageSize: 10, // 每页显示5条数据
      itemCount: props.data.length, // 总数据项数，需要根据实际数据进行设置
    });
    return {
      columns: createColumns({
        showShortcut(rowData) {
          console.log({ rowData });
        },
      }),
      pagination,
      data: props.data,
    };
  },
});
</script>
