import time


class KeepAlive:
    def __init__(self):
        self.camera_device_last_seen = {}
        self.temperature_device_last_seen = {}

    def keepalive(self, device, type, time):
        if type == 'camera':
            self.camera_device_last_seen[device] = time;
        elif type == 'temperature':
            self.temperature_device_last_seen[device] = time;



    def get_status(self):
        merged_device_status = {}

        current_time = time.time()
        for device, last_seen in self.camera_device_last_seen.items():
            merged_device_status.setdefault(device, {})['camera_status'] = int(current_time) - last_seen > 8 if 0 else 1

        for device, last_seen in self.temperature_device_last_seen.items():
            merged_device_status.setdefault(device, {})['sensor_status'] = int(current_time) - last_seen > 8 if 0 else 1

        return merged_device_status

