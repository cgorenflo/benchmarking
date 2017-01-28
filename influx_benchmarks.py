import time

from influxdb import InfluxDBClient
from iss4e.util.config import load_config

import module_locator

config = load_config(module_locator.module_path())


def execute(output, query, constraints):
    imeis = [str(imei).zfill(4) for imei in range(1000)]
    for imei in imeis:
        q = query.format(imei=imei, constraints = constraints)
        start = time.perf_counter()
        client.query(q)
        end = time.perf_counter()
        output.write(str(end - start) + "\n")


with InfluxDBClient.connect(**config["webike.influx"]) as client:


    measurement = config["webike.influx.measurement"]
    query = "select latgps, longgps from {measurement} where imei= '{imei}' and {constraints}}".format(
        measurement=measurement)

    with open("one_day_no_constraint.txt", 'w') as output:
        constraints = "time > '2016-10-18' and time < '2016-10-20'"
        execute(output, query, constraints)

    with open("one_day_with_constraint.txt", 'w') as output:
        constraints = "time > '2016-10-18' and time < '2016-10-20' and dischargecurrent > 500"
        execute(output, query, constraints)

    with open("full_week_no_constraint.txt", 'w') as output:
        constraints = "true"
        execute(output, query, constraints)

    with open("full_week_with_constraint.txt", 'w') as output:
        constraints = "dischargecurrent > 500"
        execute(output, query, constraints)
