import os
import requests
import locale
import jpholiday
from datetime import date, datetime
from typing import List, Tuple


INCOMMING_WEBHOOK_URL = os.environ['INCOMMING_WEBHOOK_URL']

# date.strftime('%a') で日本語取得するために設定する
# https://docs.python.org/ja/3.7/library/locale.html
locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')

def lambda_handler(event, context):
    candidate_date = get_candidate_date()

    (title, message) = create_message(candidate_date)
    print(title, message)

    post_slack(title, message)


def get_candidate_date() -> List[datetime.date]:
    """候補日のリストを取得する"""
    candidate_date = []
    # 8〜24日から候補日を決める
    for target_day in range(8, 24):
        target_date = get_target_date(target_day)
        if is_working_day(target_date):
            # 平日のみ候補日とする
            candidate_date.append(target_date)
    return candidate_date

def is_working_day(target: datetime.date) -> bool:
    """指定した日付が休日かどうか判定する"""
    if target.weekday() >= 5:
        # 土曜 or 日曜
        return False
    if jpholiday.is_holiday(target):
        # 祝日
        return False
    return True

def get_target_date(target: int) -> datetime.date:
    """指定した日から日付を取得する"""
    return date.today().replace(day=target)

def create_message(candidate_date: List[datetime.date]) -> Tuple[str, str]:
    """SlackにPOSTするメッセージを作成する"""
    detail = []
    for item in candidate_date:
        detail.append(item.strftime('%m/%d(%a) 12:00-13:00'))
    return (
        '次回の調整さんを作りましょう〜。',
        '\n'.join(detail)
    )

def post_slack(title: str, detail: str) -> None:
    """SlackにメッセージをPOSTする"""
    # https://api.slack.com/incoming-webhooks
    # https://api.slack.com/docs/message-formatting
    # https://api.slack.com/docs/messages/builder
    payload = {
        # https://www.webfx.com/tools/emoji-cheat-sheet/
        'icon_emoji': ':jack_o_lantern:',
        'attachments': [
            {
                'title': '調整さん',
                'title_link': 'https://chouseisan.com/',
                'color': '#36a64f',
                'pretext': title,
                'text': detail
            }
        ]
    }
 
    url = f'https://{INCOMMING_WEBHOOK_URL}'

    # http://requests-docs-ja.readthedocs.io/en/latest/user/quickstart/
    try:
        response = requests.post(url, data=json.dumps(payload))
    except requests.exceptions.RequestException as e:
        print(e)
    else:
        print(response.status_code)
