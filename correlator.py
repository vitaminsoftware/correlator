"""The correlator (between work being done and work being Toggl'ed)

Usage:
  correlator.py <user_name> <start_date> <end_date>
  correlator.py (-h | --help)

"""

import datetime
from dateutil import parser
import json
import pprint
import time

from docopt import docopt

from config import USERS
from slack_utils import get_slack_users, load_slack_channels_archive, get_user_messages
from toggl_utils import load_toggl_archive, get_user_entries

SLACK_USERS = get_slack_users()

def slack_message_toggled(slack_message, toggl_archive):
    for archive_entry in toggl_archive:
        if float(slack_message['ts']) < float(archive_entry['_start_ts_']):
            continue
        if float(slack_message['ts']) > float(archive_entry['_end_ts_']):
            continue
        return True
    return False

def print_non_toggled_messages(user, start_date, end_date):
    slack_handle = USERS[user]['slack']
    toggl_email = USERS[user]['toggl']

    slack_archive = load_slack_channels_archive()
    user_id = SLACK_USERS[slack_handle]
    slack_archive = get_user_messages(user_id, slack_archive, start_date, end_date)

    toggl_archive = load_toggl_archive()
    toggl_entries = get_user_entries(toggl_email, toggl_archive, start_date, end_date)

    for message in slack_archive:
        if not slack_message_toggled(message, toggl_entries):
            print '%s - #%s - %s' % (
                datetime.datetime.fromtimestamp(float(message['ts'])).strftime('%Y-%m-%d %H:%M:%S'),
                message['_channel_'],
                message['text']
            )

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Correlator 0.1')
    start_timestamp = time.mktime(parser.parse(arguments['<start_date>'] + ' 00:00:00').timetuple())
    end_timestamp = time.mktime(parser.parse(arguments['<end_date>'] + ' 23:59:59').timetuple())
    print_non_toggled_messages(arguments['<user_name>'], start_timestamp, end_timestamp)