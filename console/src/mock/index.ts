import Mock from "mockjs";

Mock.mock("/visualization", "get", {
  status: 200, // 自定义状态码
  message: "请求成功", // 自定义消息
  data: {
    "deviceData|5": [
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
  },
});
