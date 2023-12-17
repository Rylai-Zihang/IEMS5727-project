import Mock from "mockjs";
import faker from "faker";

const now = Date.now();
const threeMinutesAgo = now - 3 * 60 * 1000;
const thirtySeconds = 30 * 1000;

const temperatureData = Array.from({ length: 5 }, (_, deviceIndex) => {
  const deviceData = Array.from({ length: 10 }, (_, index) => ({
    time: Mock.Random.datetime(`${new Date(threeMinutesAgo + index * thirtySeconds).toISOString()}`),
    device: `Device ${String.fromCharCode(65 + deviceIndex)}`,
    temperature: Mock.Random.integer(10, 200),
  }));
  return deviceData;
});

Mock.mock("/visualization", "get", {
  status: 200, // 自定义状态码
  message: "请求成功", // 自定义消息
  data: {
    "deviceWarningData|5": [
      {
        "device|+1": ["Device A", "Device B", "Device C", "Device D", "Device E"],
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
        "name|+1": ["Device A", "Device B", "Device C", "Device D", "Device E"],
        "value|10-100": 10,
      },
    ],
    "logData|5": [
      {
        time: "@datetime",
        "device|+1": ["Device A", "Device B", "Device C", "Device D", "Device E"],
        "level|+1": ["Low", "Medium", "High"],
        "dealt|+1": ["true", "false"],
        shortcut: faker.image.dataUri(100, 100),
      },
    ],
    temperatureData,
    totalData: 9999,
    "aliveData|5": [
      {
        "device|+1": ["Device A", "Device B", "Device C", "Device D", "Device E"],
        "camera_status|+1": [0, 1],
        "sensor_status|+1": [0, 1],
      },
    ],
  },
});
