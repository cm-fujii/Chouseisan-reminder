import json
import os
import requests
import locale
import jpholiday
from datetime import date, datetime, timedelta
from typing import List, Tuple


INCOMMING_WEBHOOK_URL = os.environ['INCOMMING_WEBHOOK_URL']

# date.strftime('%a') で日本語取得するために設定する
# https://docs.python.org/ja/3.7/library/locale.html
locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')

def lambda_handler(event, context):
    # 最初の平日以外なら通知しない
    if is_first_working_day(date.today()) is False:
        return

    # 候補日のリストを取得する
    candidate_date = get_candidate_date()
    # メッセージを作成する
    (title, message) = create_message(candidate_date)
    # Slackに通知する
    post_slack(title, message)

def is_first_working_day(today: datetime.date) -> bool:
    """指定日がその月の最初の平日か判定する"""
    for target_day in range(1, today.day + 1):
        if is_working_day(today.replace(day=target_day)):
            if target_day == today.day:
                # その月で最初の平日である
                return True
            # その月で2回目以降の平日である
            return False
    # 平日ではない
    return False

def get_candidate_date() -> List[datetime.date]:
    """候補日のリストを取得する"""
    candidate_date = []
    # 8〜24日から候補日を決める
    for target_day in range(8, 25):
        target_date = get_target_date(target_day)
        if is_working_day(target_date):
            # 平日のみ候補日とする
            candidate_date.append(target_date)
    return candidate_date

def is_working_day(target: datetime.date) -> bool:
    """指定日が休日か判定する"""
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

    vol = get_vol(date(2019, 1,1 ), date.today())

    return (
        '次回の調整さんを作りましょう〜。',
        f'201901JOIN雑談会Vol.{vol}\n\n' +
        '\n'.join(detail)
    )

def get_vol(base: datetime.date, target: datetime.date) -> int:
    """次回開催の番号を取得する"""
    return (target.year - base.year) * 12 + target.month - base.month - 1

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
