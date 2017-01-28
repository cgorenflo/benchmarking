import time

from iss4e.db import influxdb
from iss4e.util.config import load_config

import module_locator

config = load_config(module_locator.module_path())


def execute(output):
    measurement = config["webike.measurement"]
    imeis = [str(imei).zfill(4) for imei in range(1000)]
    points = ({
        "measurement":measurement,
        "tags":{"imei":imei},
        "accelx": 0.0,
        "accely": 0.0,
        "accelz": 0.0,
        "atmospress": 0.0,
        "batteryvoltage": 0.0,
        "chargingcurrent": 0,
        "codeversion": 0,
        "dischargecurrent": 0,
        "gravaccel": 0.0,
        "gyrox": 0.0,
        "gyroy": 0.0,
        "gyroz": 0.0,
        "latgps": 0.0,
        "latnetwork": 0.0,
        "light": 0,
        "linaccelx": 0.0,
        "linaccely": 0.0,
        "linaccelz": 0.0,
        "longgps": 0.0,
        "longnetwork": 0.0,
        "magx": 0.0,
        "magy": 0.0,
        "magz": 0.0,
        "phonebattstate": '"false"',
        "phoneipaddress": '"1.1.1.1"',
        "proximity": 0,
        "tempbattery": 0.0,
        "tempbox": 0.0} for imei in imeis)

    start = time.perf_counter()
    client.write_points(points)
    end = time.perf_counter()
    output.write(str(end - start) + "\n")

with influxdb.connect(**config["webike.influx"]) as client:
    with open("insert.txt", 'w') as output:
        execute(output)
