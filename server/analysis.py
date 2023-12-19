# 一个简单的风险指数计算模型：
# 假设我们定义的风险指数 ( R ) 是温度 ( T ) 和火焰检测置信度 ( F ) 的函数，可以表示为：
# [ R = w_T \cdot T + w_F \cdot F ]
# 其中，( w_T ) 和 ( w_F ) 是对应于温度和火焰检测置信度的权重系数。这些权重决定了每个因素对于风险指数的影响。
# 为了简化，我们可以假设 ( w_T )=0.4 和 ( w_F )=0.6，即：
# [ R = 0.4 \cdot T + 0.6 \cdot F ]
# 由于火焰检测置信度 ( F ) 的范围是 0 到 1.0，而温度 ( T ) 的范围是 0 到 100，直接相加可能会导致温度对结果的影响过于显著。
# 为了平衡这两个因素的贡献，我们可以对它们进行归一化，使它们的范围一致，例如：
# [ R = w_T \cdot \frac{T}{100} + w_F \cdot F ]
# 这个简单的模型会将温度和火焰检测置信度相加，得到一个介于 0 到 1.0 之间的风险指数。再乘以100归一化道0-100的范围输出.


def analysis_risk(temperatures, fires):
    print(temperatures)
    print(fires)

    # 初始化一个字典来保存设备和其对应的平均温度和火焰检测置信度
    device_data = {}

    # 处理温度数据
    for device_temps in temperatures:
        device = device_temps[0]['device']
        avg_temp = sum([t['temperature'] for t in device_temps]) / len(device_temps)
        device_data[device] = {'temperature': avg_temp}

    # 处理火焰检测置信度数据
    for entry in fires:
        device = entry['device']
        if device not in device_data:
            device_data[device] = {}
        if 'conv' not in device_data[device]:
            device_data[device]['conv'] = []
        device_data[device]['conv'].append(entry['conv'])

    # 计算平均火焰检测置信度
    for device, data in device_data.items():
        if 'conv' in data:
            data['conv'] = sum(data['conv']) / len(data['conv'])

    # 计算每个设备的风险指数，并将其标准化到0到100的范围内
    def calculate_normalized_risk_index(temp, conv):
        # 使用一个简单的线性组合模型来计算原始风险指数
        raw_risk_index = 0.4 * temp / 100 + 0.6 * conv
        # 将风险指数标准化到0到100的范围内
        normalized_risk_index = raw_risk_index * 100  # 因为最大可能的风险指数是1
        return min(max(normalized_risk_index, 0), 100)  # 限制在0到100之间

    # 存储设备风险指数的列表
    risk_data = []

    # 为每个设备计算风险指数
    for device, data in device_data.items():
        if 'temperature' in data and 'conv' in data:
            risk_index = calculate_normalized_risk_index(data['temperature'], data['conv'])
            risk_data.append({
                "name": device,
                "value": round(risk_index)  # 四舍五入到最接近的整数
        })

    # 输出风险数据
    print(risk_data)

    return risk_data

    # return [
    #     {
    #       "name": "Device A",
    #       "value": 28
    #     },
    #     {
    #       "name": "Device B",
    #       "value": 20
    #     },
    #     {
    #       "name": "Device C",
    #       "value": 41
    #     },
    #     {
    #       "name": "Device D",
    #       "value": 57
    #     },
    #     {
    #       "name": "Device E",
    #       "value": 89
    #     }
    # ]
