#!/usr/bin/python

from datetime import datetime

DAYS_OF_MONTH = 30
MONTHS_OF_YEAR = 12
SECONDS_OF_MINUTE = 60

class Birth(object):
    def __init__(self, user_datetime):
        """Constructor for Birth class.

        Args:
            user_datetime: datetime.datetime object.
        """
        self._user_datetime = user_datetime
        self._birth = datetime(2008, 5, 29, 14, 15)
        self._delta = self._user_datetime - self._birth

    def _format_string(self, item, label):
        if item == 0:
            return ""
        elif item > 1:
            return "%d %ss " % (item, label)
        else:
            return "%d %s " % (item, label)

    def _process_days(self, days):
        """Calculate days to return a tuple (year, month, day).

        Args:
            days: How many days to calculate.

        Returns:
            A tuple (yesr, month, day).
        """
        year = 0
        month = 0
        day = 0

        if days < DAYS_OF_MONTH:
            day = days
        else:
            day = days % DAYS_OF_MONTH
            month = days / DAYS_OF_MONTH
            if month > MONTHS_OF_YEAR:
                month = month % MONTHS_OF_YEAR
                year = month / MONTHS_OF_YEAR

        return (year, month, day)

    def _process_seconds(self, seconds):
        """Calculate seconds to return a tuple (hour, minute, second).

        Args:
            seconds: How many seconds to calculate.

        Returns:
            A tuple (hour, minute, second).
        """
        hour = 0
        minute = 0
        second = 0
        if seconds < SECONDS_OF_MINUTE:
            second = seconds
        else:
            second = seconds % SECONDS_OF_MINUTE
            minute = seconds / SECONDS_OF_MINUTE
            if minute > SECONDS_OF_MINUTE:
                minute = minute % SECONDS_OF_MINUTE
                hour = minute / SECONDS_OF_MINUTE

        return (hour, minute, second)

    def __str__(self):
        year, month, day = self._process_days(self._delta.days)
        hour, minute, second = self._process_seconds(self._delta.seconds)

        str = self._format_string(year, "Year") + self._format_string(month, "Month") + \
              self._format_string(day, "Day") + self._format_string(hour, "Hour") + \
              self._format_string(minute, "Minute") + self._format_string(second, "Second")
        return str


def create(user_datetime=datetime.now()):
    """
    Constructs a Birth object based on the argument.

    Args:
        user_datetime: datetime.datetime object. Default is datetime.datetime.now.

    Returns:
        Birth object.
    """
    return Birth(user_datetime)

if __name__ == '__main__':
    birth = create()
    print birth
