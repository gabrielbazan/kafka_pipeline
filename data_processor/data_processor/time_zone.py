from typing import Optional

from timezonefinder import TimezoneFinder


class TimeZoneException(Exception):
    pass


timezone_finder = TimezoneFinder(in_memory=True)


def get_timezone(latitude: float, longitude: float) -> str:
    timezone: Optional[str] = timezone_finder.timezone_at(lng=longitude, lat=latitude)

    if timezone is None:
        raise TimeZoneException("Could not determine timezone")

    return timezone
