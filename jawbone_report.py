import datetime
import dateutil.parser
from pprint import pprint

from kiefer.auth import KieferAuth
from kiefer.client import KieferClient

import secrets


def main():
    #print(get_access_token())
    pprint(daily_sleep_report(), width=240)


def get_access_token():
    auth = KieferAuth('jawbone_secrets.json')
    return auth.get_access_token()


def daily_sleep_report(start_date=None, end_date=None):
    if not start_date:
        today = datetime.date.today()
        start_date = datetime.date(year=today.year, month=today.month, day=1)

    start_time = date_to_unix_time(start_date)

    end_time = None
    if end_date:
        end_time = date_to_unix_time(end_date + datetime.timedelta(days=1))

    client = KieferClient(secrets.jawbone_access_token)
    resp = client.get_sleeps(start_time=start_time, end_time=end_time,
                             limit=100)
    stats = {}
    for day_dict in resp['data']['items']:
        (date, day_stats) = extract_daily_sleep_stats(day_dict)
        if date and day_stats:
            stats[date] = day_stats

    return stats


def extract_daily_sleep_stats(day_dict):
    date = dateutil.parser.parse(str(day_dict['date'])).date()
    xid = day_dict['xid']

    d = day_dict['details']
    stats = {
        'sleep_begin_time': unix_time_to_time_string(d['awake_time']),
        'sleep_wake_time': unix_time_to_time_string(d['asleep_time']),
        'sleep_amount_total': '%0.2f' % (d['duration'] / 3600.0),
        'sleep_amount_deep': '%0.2f' % (d['sound'] / 3600.0),
        'sleep_amount_light': '%0.2f' % (d['light'] / 3600.0),
        'sleep_amount_awake': '%0.2f' % (d['awake'] / 3600.0)
    }

    return (date, stats)


# Utilities
def date_to_unix_time(date):
    EPOCH_TIME = datetime.date(1970, 1, 1)
    return (date - EPOCH_TIME).total_seconds()


def unix_time_to_datetime(time):
    return datetime.datetime.fromtimestamp(time)


def unix_time_to_date(time):
    return datetime.date.fromtimestamp(time)


def datetime_to_time_string(datetime):
    return datetime.strftime('%I:%M %p')


def unix_time_to_time_string(time):
    return datetime_to_time_string(unix_time_to_datetime(time))


if __name__ == '__main__':
    main()
