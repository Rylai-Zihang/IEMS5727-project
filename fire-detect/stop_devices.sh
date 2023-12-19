#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 DeviceA [DeviceB ...]"
    exit 1
fi

for device in "$@"; do
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

    pkill -f "$script $device"
done