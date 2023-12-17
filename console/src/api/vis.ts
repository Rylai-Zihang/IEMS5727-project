import request from "@/utils/request";
import Mock from "mockjs";

export const getVisualization = () => {
  return request({
    url: "/api/query/analyse_data",
  });
};
