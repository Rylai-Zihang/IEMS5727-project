#!/bin/bash

# 检查是否有参数传入
if [ $# -eq 0 ]; then
    echo "Usage: $0 DeviceA [DeviceB ...]"
    exit 1
fi

# 遍历所有参数
for device in "$@"; do
    # 根据设备名决定要运行的脚本
    case $device in
        DeviceA)
            script="camera_device.py"
            ;;
        DeviceB|DeviceC|DeviceD|DeviceE)
            script="mock_camera_device.py"
            ;;
        *)
            echo "Unknown device: $device"
            continue
            ;;
    esac

    # 启动设备脚本，并将输出重定向到日志文件
    python3 $script $device > "${device}.log" 2>&1 &
done