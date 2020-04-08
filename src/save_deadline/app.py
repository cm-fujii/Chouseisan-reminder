import boto3
import json
import logging
import os
import re

from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')

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

    if 'reminder_misc_join_201901_workflow' != body['event']['username']:
        logger.info('No workflow message.')
        return

    deadline = parse_timestamp(body['event']['text'])
    url = parse_url(body['event']['text'])
    logger.info(f'deadline: {deadline}, url: {url}')

    # 当日10時をDynamoDBのTTL期限とする
    expiration = deadline + 60*60*10

    put_item(deadline, url, expiration)


def parse_timestamp(text):
    pattern = r'.+\n期限は \*(\d{4}/\d{1,2}/\d{1,2})\* です！'
    res = re.match(pattern, text)
    if res:
        # 0時のunixtimeを返す
        return int(datetime.strptime(res.group(1), '%Y/%m/%d').timestamp())
    raise ValueError


def parse_url(text):
    pattern = r'.+\n.+\n<(.+)>'
    res = re.match(pattern, text)
    if res:
        return res.group(1)
    raise ValueError

def put_item(deadline, url, expiration):
    table_name = os.environ['REMINDER_TABLE_NAME']
    table = dynamodb.Table(table_name)
    res = table.put_item(Item={
        'deadline': deadline,
        'expiration': expiration,
        'url': url
    })
    logger.info(res)
