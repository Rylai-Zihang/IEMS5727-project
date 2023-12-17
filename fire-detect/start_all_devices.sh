#!/bin/bash

python3 camera_device.py DeviceA > deviceA.log 2>&1 &
python3 mock_camera_device.py DeviceB > deviceA.log 2>&1 &
python3 mock_camera_device.py DeviceC > deviceA.log 2>&1 &
python3 mock_camera_device.py DeviceD > deviceA.log 2>&1 &
python3 mock_camera_device.py DeviceE > deviceA.log 2>&1 &
