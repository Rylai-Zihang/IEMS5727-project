<template>
  <div>
    <div>【Alert Log Table】</div>
    <n-data-table :columns="columns" :data="data" :pagination="pagination" :bordered="false" />
  </div>
</template>

<script>
import { h, defineComponent, defineProps } from "vue";
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
    console.log(props.data);
    return {
      columns: createColumns({
        showShortcut(rowData) {
          console.log({ rowData });
        },
      }),
      pagination: false,
      data: props.data,
    };
  },
});
</script>
