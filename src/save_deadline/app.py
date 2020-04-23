import boto3
import json
import logging
import os
import re

from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')

SLACK_WORKFLOW_USER_DEADLINE = 'reminder_misc_join_201901_workflow'
SLACK_WORKFLOW_USER_ANNOUNCE = '同期会のお知らせ'

SLACK_WORKFLOW_USERS = [
    SLACK_WORKFLOW_USER_DEADLINE,
    SLACK_WORKFLOW_USER_ANNOUNCE
]

def lambda_handler(event, context):
    main(event)
    return {
        'statusCode': 200
    }

def main(event):
    logger.info(json.dumps(event))

    body = json.loads(event['body'])
    logger.info(json.dumps(body))

    if 'username' not in body['event']:
        logger.info('No username.')
        return

    if body['event']['username'] not in SLACK_WORKFLOW_USERS:
        logger.info('No workflow message.')
        return

    if body['event']['username'] == SLACK_WORKFLOW_USER_DEADLINE:
        # 調整さんの締切とURLを登録する
        deadline = parse_timestamp_for_deadline(body['event']['text'])
        url = parse_url_for_deadline(body['event']['text'])
        item = {
            'deadline': deadline,
            'type': 'deadline',
            'expiration': deadline + 60*60*11,  # 当日11時をDynamoDBのTTL期限とする
            'url': url
        }
        logger.info(f'item for deadline: {json.dumps(item)}')

    if body['event']['username'] == SLACK_WORKFLOW_USER_ANNOUNCE:
        # 開催日を登録する
        announce = parse_timestamp_for_announce(body['event']['text'])
        item = {
            'deadline': announce,
            'type': 'announce',
            'expiration': announce + 60*60*11,  # 当日11時をDynamoDBのTTL期限とする
        }
        logger.info(f'item for announce: {json.dumps(item)}')

    put_item(item)


def parse_timestamp_for_deadline(text):
    pattern = r'.+\n期限は \*(\d{4}/\d{1,2}/\d{1,2})\* です！'
    res = re.match(pattern, text)
    if res:
        # 0時のunixtimeを返す
        return int(datetime.strptime(res.group(1), '%Y/%m/%d').timestamp())
    raise ValueError

def parse_timestamp_for_announce(text):
    pattern = r'同期会の開催日は \*(\d{4}/\d{1,2}/\d{1,2})\* です！'
    res = re.match(pattern, text)
    if res:
        # 0時のunixtimeを返す
        return int(datetime.strptime(res.group(1), '%Y/%m/%d').timestamp())
    raise ValueError

def parse_url_for_deadline(text):
    pattern = r'.+\n.+\n<(.+)>'
    res = re.match(pattern, text)
    if res:
        return res.group(1)
    raise ValueError

def put_item(item):
    table_name = os.environ['REMINDER_TABLE_NAME']
    table = dynamodb.Table(table_name)
    res = table.put_item(Item=item)
    logger.info(res)
