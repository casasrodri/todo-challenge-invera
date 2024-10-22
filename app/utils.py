from datetime import datetime

from django.utils.timezone import make_aware


def get_date(date_str: str) -> datetime:
    """Convert a string date to a datetime object.

    Args:
        date_str (str): Date in string format.

    Returns:
        datetime: Datetime object.
    """
    return make_aware(datetime.strptime(date_str, "%Y-%m-%d"))
