import Mock from "mockjs";
import faker from "faker";

const now = Date.now();
const threeMinutesAgo = now - 3 * 60 * 1000;
const thirtySeconds = 30 * 1000;
const devices = ["Device A", "Device B", "Device C", "Device D", "Device E"];

const temperatureData = Array.from({ length: 5 }, (_, deviceIndex) => {
  const deviceData = Array.from({ length: 10 }, (_, index) => ({
    time: Mock.Random.datetime(`${new Date(threeMinutesAgo + index * thirtySeconds).toISOString()}`),
    device: `Device ${String.fromCharCode(65 + deviceIndex)}`,
    temperature: Mock.Random.integer(10, 200),
  }));
  return deviceData;
});

Mock.mock("/api/query/analyse_data/mock", "get", {
  status: 200, // 自定义状态码
  message: "请求成功", // 自定义消息
  data: {
    "deviceWarningData|5": [
      {
        "device|+1": devices,
        "warningLevels|3": [
          {
            "name|+1": ["Low", "Medium", "High"],
            "value|10-100": 10,
          },
        ],
      },
    ],
    "riskData|5": [
      {
        "name|+1": devices,
        "value|10-100": 10,
      },
    ],
    "logData|5": [
      {
        time: "@datetime",
        "device|+1": devices,
        "level|+1": ["Low", "Medium", "High"],
        "dealt|+1": ["true", "false"],
        shortcut: faker.image.dataUri(100, 100),
      },
    ],
    temperatureData,
    totalData: 9999,
    aliveData: {
      [devices[0]]: {
        camera_status: "@pick([0, 1])",
      },
      [devices[1]]: {
        camera_status: "@pick([0, 1])",
      },
      [devices[2]]: {
        camera_status: "@pick([0, 1])",
      },
      [devices[3]]: {
        camera_status: "@pick([0, 1])",
      },
      [devices[4]]: {
        camera_status: "@pick([0, 1])",
      },
    },
  },
});
