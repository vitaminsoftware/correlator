import csv
import copy
import datetime
from dateutil import parser
import datetime
import os
import time

from config import TOGGL_EXPORT_DIR

def load_toggl_archive():
    result = []
    archives = os.listdir(TOGGL_EXPORT_DIR)
    for archive in archives:
        archive_file_path = TOGGL_EXPORT_DIR + '/' + archive
        with open(archive_file_path, 'rt') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row_copy = copy.deepcopy(row)
                try:
                    start_ts = time.mktime(parser.parse(row['Start date'] + ' ' + row['Start time']).timetuple())
                except ValueError:
                    print('%s %s cannot be parsed as start time for activtiy: %r' % (row['Start date'], row['Start time'], row))

                try:
                    end_ts = time.mktime(parser.parse(row['End date'] + ' ' + row['End time']).timetuple())
                except ValueError:
                    print('%s %s cannot be parsed as end time for activtiy: %r' % (row['End date'], row['End time'], row))

                row_copy['_start_ts_'] = start_ts
                row_copy['_end_ts_'] = end_ts
                result += [row_copy]
    return result

def get_user_entries(user_email, toggl_archive, start_ts=None, end_ts=None):
    result = []
    for archive_entry in toggl_archive:
        if start_ts is not None and archive_entry['_end_ts_'] < start_ts:
            continue
        if end_ts is not None and archive_entry['_start_ts_'] > end_ts:
            continue
        if archive_entry['Email'] == user_email:
            result += [archive_entry]

    return result