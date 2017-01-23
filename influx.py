from iss4e.db import influxdb
from iss4e.util.config import load_config

import module_locator

config = load_config(module_locator.module_path())

with influxdb.connect(**config["webike.influx"]) as client:
    for imei in range(1000):
        client.query("SELECT * INTO benchmarks..webike FROM webike..webike_benchmarking where imei='{imei}' group by imei".format(imei=str(imei).zfill(4)))
