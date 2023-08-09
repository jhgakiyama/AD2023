from math import trunc
import time
import datetime


API = "cc3d07bf7909e147cd7443c0415b0f76"

coordList = ["lat=31&lon=64", "lat=40&lon=-73", "lat=-31&lon=-64",
             "lat=25&lon=64", "lat=-34&lon=-58", "lat=19&lon=-99",
             "lat=53&lon=6", "lat=41&lon=44", "lat=4&lon=74",
             "lat=35&lon=139"]

cityList = ["London", "New%20York", "Cordoba", "Taipei", "Buenos%20Aires",
            "Mexico%20City", "Dublin", "Tiflis", "Bogota", "Tokio"]

lat_r, long_r = -27.46056, -58.98389
rcia = [f"lat={lat_r}&lon={long_r}"]


def datetime_to_unixtime(fecha_hora):
    return trunc(time.mktime(fecha_hora.timetuple()))


def unixtime_to_datetime(unix_time):
    return datetime.fromtimestamp(unix_time)
