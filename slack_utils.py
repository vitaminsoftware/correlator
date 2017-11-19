import copy
import json
import os

from config import SLACK_EXPORT_DIR

def get_slack_users():
    slack_users_file = SLACK_EXPORT_DIR + '/users.json'
    with open(slack_users_file, 'rt') as f:
        raw_user_data = json.loads(f.read())
        result = {}
        for raw_user in raw_user_data:
            result[raw_user['name']] = raw_user['id']
        return result

def load_slack_channels_archive():
    slack_channels_file = SLACK_EXPORT_DIR + '/channels.json'
    result = {}
    with open(slack_channels_file, 'rt') as f:
        raw_channel_data = json.loads(f.read())
        for raw_channel in raw_channel_data:
            name = raw_channel['name']
            result[name] = []
            slack_channel_folder = SLACK_EXPORT_DIR + '/' + name
            slack_channel_files = os.listdir(slack_channel_folder)
            for file_name in slack_channel_files:
                slack_channel_file_path = slack_channel_folder + '/' + file_name
                with open(slack_channel_file_path, 'rt') as g:
                    messages = json.loads(g.read())
                    result[name] += messages
    return result

def get_user_messages(slack_user_id, channels_archive, start_ts=None, end_ts=None):
    result = []
    for channel, messages in channels_archive.iteritems():
        for message in messages:
            if start_ts is not None and float(message['ts']) < start_ts:
                continue
            if end_ts is not None and float(message['ts']) > end_ts:
                continue
            if message.get('user') == slack_user_id:
                message_copy = copy.deepcopy(message)
                message_copy['_channel_'] = channel
                result += [message_copy]
    return sorted(result, key=lambda m: float(m['ts']))