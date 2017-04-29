import argparse
import logging
import datetime
import calendar
import socket
from collections import defaultdict
from pprint import pprint, pformat
import smtplib
from email.mime.text import MIMEText

import movesapp_report
import jawbone_report


def main():
    parser = argparse.ArgumentParser(description='Daily report')

    parser.add_argument('--moves-token', action="store_true", default=False,
                        help='generate new access token for Moves API')

    options = parser.parse_args()
    if options.moves_token:
        print movesapp_report.get_access_token()
        return

    daily_report()


def daily_report(today=None):
    if today is None:
        today = datetime.date.today()
    start_date = datetime.date(year=today.year, month=today.month, day=1)
    #days_in_month = calendar.monthrange(today.year, today.month)[1]
    #end_date = start_date + datetime.timedelta(days=days_in_month)
    date_range = (start_date + datetime.timedelta(days=ofs)
                 for ofs in xrange((today - start_date).days + 1))

    movesapp_stats = movesapp_report.daily_places_report(today=today)
    jawbone_stats = jawbone_report.daily_sleep_report(start_date=start_date)

    # Merge stats dicts.
    stats = defaultdict(dict)
    for report_stats in (movesapp_stats, jawbone_stats):
        for (date, day_stats) in report_stats.iteritems():
            stats[date].update(day_stats)

    # Add date field as string.
    for (date, day_stats) in stats.iteritems():
        day_stats['date'] = date.strftime('%a %Y-%m-%d')

    lines = []
    for date in date_range:
        if date in stats:
            lines.append(pformat(stats[date], width=240))
        else:
            lines.append('---')

    buf = '\n'.join(lines)

    print(buf)
    send_email('daily report', buf)


def send_email(subject, body, recipient='qqrsmith@gmail.com'):
    msg = MIMEText(body)
    msg['To'] = recipient
    msg['From'] = 'dailyreport@gifball.com'
    msg['Subject'] = subject

    try:
        server = smtplib.SMTP('localhost')
    except socket.error:
        logging.warn('No SMTP server found on localhost')
        return

    #server.set_debuglevel(True) # show communication with the server
    try:
        server.sendmail(msg['From'], [recipient], msg.as_string())
    finally:
        server.quit()


if __name__ == '__main__':
    main()
