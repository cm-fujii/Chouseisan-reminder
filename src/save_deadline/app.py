import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(json.dumps(event))

    body = json.loads(event['body'])

    return {
        'statusCode': 200,
        'body': json.dumps(
            {'challenge': body['challenge']},
        ),
    }
