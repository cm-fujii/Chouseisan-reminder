import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(json.dumps(event))

    body = json.loads(event['body'])
    logger.info(json.dumps(body))

    return {
        'statusCode': 200
    }
