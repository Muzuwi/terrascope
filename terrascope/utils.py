import os
import datetime


# Instance folder path, to keep stuff aware from flask app.
INSTANCE_FOLDER_PATH = os.path.join("/tmp", "terrascope-instance")


def get_current_time():
    return datetime.datetime.utcnow()


def pretty_date(dt, default=None):
    # Returns string representing "time since" eg 3 days ago, 5 hours ago etc.

    if default is None:
        default = "just now"

    now = datetime.datetime.utcnow()
    diff = now - dt

    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:

        if not period:
            continue

        if int(period) >= 1:
            if int(period) > 1:
                return "%d %s ago" % (period, plural)
            return "%d %s ago" % (period, singular)

    return default
