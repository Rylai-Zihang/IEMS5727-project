import time


class KeepAlive:
    def __init__(self):
        self.camera_device_last_seen = {}
        self.temperature_device_last_seen = {}

    def keepalive(self, device, type, time):
        if type == 'camera':
            self.camera_device_last_seen[device] = time;
        elif type == 'sensor':
            self.temperature_device_last_seen[device] = time;



    def get_status(self):
        merged_device_status = {}

        current_time = time.time()
        for device, last_seen in self.camera_device_last_seen.items():
            camera_status = 0 if int(current_time) - int(last_seen) > 8  else 1
            print(self.temperature_device_last_seen.get(device, 0), current_time)
            sensor_status =  0 if int(current_time) - int(self.temperature_device_last_seen.get(device, 0)) > 8 else 1
            merged_device_status[device] = {
                'camera_status': camera_status,
                'sensor_status': sensor_status,
            }

        return merged_device_status

