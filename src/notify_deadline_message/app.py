import boto3
import json
import logging
import os
import requests

from botocore.exceptions import ClientError
from datetime import date, datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

INCOMMING_WEBHOOK_URL = os.environ['INCOMMING_WEBHOOK_URL']

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    today = get_today()
    logger.info(f'today: {today}')

    remind_data = get_remind_data(today)
    logger.info(f'get_remind_data(): {remind_data}')

    if remind_data is None:
        return

    # Slackに通知する
    post_slack(remind_data)


def get_today():
    today = date.today()
    # 今日の0時0分0秒のunixtimeを返す
    return int(datetime(today.year, today.month, today.day).timestamp())


def get_remind_data(deadline):
    table_name = os.environ['REMINDER_TABLE_NAME']
    table = dynamodb.Table(table_name)
    try:
        res = table.get_item(Key={
                'deadline': deadline
            }
        )
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        return None
    else:
        return res.get('Item', None)


def post_slack(remind_data):
    # https://api.slack.com/incoming-webhooks
    # https://api.slack.com/docs/message-formatting
    # https://api.slack.com/docs/messages/builder
    payload = {
        # https://www.webfx.com/tools/emoji-cheat-sheet/
        'icon_emoji': ':bangbang:',
        'text': '<!here> 今日が締切です！！　記入お願いします！\n',
        'attachments': [
            {
                'text': remind_data['url']
            }
        ]
    }

    url = f'https://{INCOMMING_WEBHOOK_URL}'

    # http://requests-docs-ja.readthedocs.io/en/latest/user/quickstart/
    try:
        response = requests.post(url, data=json.dumps(payload))
    except requests.exceptions.RequestException as e:
        logger.error(e)
    else:
        logger.info(response.status_code)
