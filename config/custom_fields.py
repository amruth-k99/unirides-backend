from django.db import models
from datetime import datetime


class CustomDateTimeField(models.DateTimeField):
    def to_python(self, value):
        if value is not None:
            dt = str(value).split(".")
            try:
                dt_val = datetime.strptime(dt[0], "%Y-%m-%d %H:%M:%S")
            except Exception as e:
                dt_val = datetime.strptime(dt[0], "%Y-%m-%d")
            return dt_val
        else:
            return value


def format_date(value):
    try:
        if value is not None:
            dt = str(value).split(" ")

            new_dt = "T".join(dt) + "Z"

            return new_dt
        else:
            return value
    except Exception as e:
        return value


def parse_date(value):
    try:
        if value is not None:

            dt = str(value).split(" ")

            new_dt = dt[0] + "T" + dt[1]

            return new_dt
        else:
            return value
    except Exception as e:
        return value


def get_date(value):
    try:
        if value is not None:

            dt = str(value).split(" ")

            new_dt = dt[0]

            return new_dt
        else:
            return value
    except Exception as e:
        return value
