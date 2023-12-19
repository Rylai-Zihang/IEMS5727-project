# 风险等级这样算：
# temperature = 80  # 温度数据
# confidence = 0.8  # 火焰识别置信度数据

# # 定义温度和置信度的权重，用于计算风险等级
# temperatureWeight = 0.6
# confidenceWeight = 0.4
# riskLevel = temperature * temperatureWeight + confidence * confidenceWeight

# minRiskLevel = 0  # 假设最小风险等级为0
# maxRiskLevel = 100  # 假设最大风险等级为100

# # 将风险等级归一化到0-100之间
# normalizedRiskLevel = (riskLevel - minRiskLevel) / (maxRiskLevel - minRiskLevel) * 100

# print("Risk Level:", normalizedRiskLevel)


def analysis_risk(temperatures, fires):
    print(temperatures)
    print(fires)

    return [
        {
          "name": "Device A",
          "value": 28
        },
        {
          "name": "Device B",
          "value": 38
        },
        {
          "name": "Device C",
          "value": 46
        },
        {
          "name": "Device D",
          "value": 36
        },
        {
          "name": "Device E",
          "value": 89
        }
    ]
