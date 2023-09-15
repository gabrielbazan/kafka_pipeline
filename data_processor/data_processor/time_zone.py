from datetime import datetime

import pytz
from timezonefinder import TimezoneFinder


class TimeZoneException(Exception):
    pass


timezone_finder = TimezoneFinder(in_memory=True)


def to_utc(
    input_timestamp_str,
    latitude,
    longitude,
    input_timestamp_format,
    output_timestamp_format,
):
    timezone_str = timezone_finder.timezone_at(lng=longitude, lat=latitude)

    if not timezone_str:
        raise TimeZoneException("Could not determine timezone")

    input_timezone = pytz.timezone(timezone_str)

    input_timestamp_obj = datetime.strptime(input_timestamp_str, input_timestamp_format)

    localized_timestamp = input_timezone.localize(input_timestamp_obj)

    utc_timestamp_obj = localized_timestamp.astimezone(pytz.UTC)

    utc_timestamp_str = utc_timestamp_obj.strftime(output_timestamp_format)

    return utc_timestamp_str
