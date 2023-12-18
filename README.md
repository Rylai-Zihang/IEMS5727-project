# This is the repo for mini-project in IEMS5727

## step1: setup database
```
cd server;
# will drop the old database automatically.
./setup_db.sh
```

## step2: start server
```
cd server;
pip install -r requirments.txt;
python3 server.py
```

## step3: start camera devices
```
cd fire-detect;
pip install -r requirments.txt;
# start all camera devices
./start_devices.sh DeviceA DeviceB DeviceC DeviceD DeviceE
```

## step4: start temperature devices
```
cd hardware;
# start all temperature devices
./start_devices.sh DeviceA DeviceB DeviceC DeviceD DeviceE
```

## step5: start console
```
cd console;
yarn;
yarn run dev;
```

## visiting console to overview the data
http://localhost:5173/console/

## step6: stop selected device to test offline
```
cd fire-detect;
./stop_devices.sh DeviceB DeviceC;
cd hardware;
./stop_devices.sh DeviceB DeviceC;
# wait for 5 seconds, then we see DeviceB & DeviceC is offline

cd fire-detect;
./start_devices.sh DeviceB DeviceC;
cd hardware;
./start_devices.sh DeviceB DeviceC;
# then refresh web console, we can see them are online

```

## step7: stop all devices
```
cd fire-detect;
./stop_devices.sh DeviceA DeviceB DeviceC DeviceD DeviceE;
cd hardware;
./stop_devices.sh DeviceA DeviceB DeviceC DeviceD DeviceE;
```