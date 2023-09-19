from timezonefinder import TimezoneFinder


class TimeZoneException(Exception):
    pass


timezone_finder = TimezoneFinder(in_memory=True)


def get_timezone(latitude: float, longitude: float) -> str:
    timezone_str = timezone_finder.timezone_at(lng=longitude, lat=latitude)

    if not timezone_str:
        raise TimeZoneException("Could not determine timezone")

    return timezone_str
