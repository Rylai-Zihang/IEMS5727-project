# This is the repo for mini-project in IEMS5727

## step1: setup database
```
cd server;
./setup_db.sh
```

## step2: start server
```
cd server;
pip install -r requirments.txt;
python3 server.py
```

## step3: mock temperature data
```
cd server;
python3 mock_data_temperature.py
```

## step4: start all devices
```
cd fire-detect;
pip install -r requirments.txt;
./start_all_devices.sh
```

## step5: start console
```
cd console;
yarn;
yarn run dev;
```

## visiting console
http://localhost:5173/console/

## step6: stop all devices
```
cd fire-detect;
./stop_all_devices.sh
```


