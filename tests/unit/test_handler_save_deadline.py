import json

import pytest

from datetime import date
from src.save_deadline import app

@pytest.mark.parametrize(
    'text, expected', [
        (
            '調整さんに記入をお願いします！\n期限は *2020/04/06* です！\n<https://chouseisan.com/s?h=xxx>',
            1586098800
        ),
        (
            '調整さんに記入をお願いします！\n期限は *2020/5/9* です！\n<https://chouseisan.com/s?h=xxx>',
            1588950000
        ),
        (
            '調整さんに記入をお願いします！\n期限は *2020/12/12* です！\n<https://chouseisan.com/s?h=xxx>',
            1607698800
        ),
    ])
def test_parse_timestamp_for_deadline(text, expected):
    actual = app.parse_timestamp_for_deadline(text)
    assert expected == actual

@pytest.mark.parametrize(
    'text, expected', [
        (
            '調整さんに記入をお願いします！\n期限は *2020/04/06* です！\n<https://chouseisan.com/s?h=xxx>',
            'https://chouseisan.com/s?h=xxx'
        ),
    ])
def test_parse_url_for_deadline(text, expected):
    actual = app.parse_url_for_deadline(text)
    assert expected == actual

@pytest.mark.parametrize(
    'text, expected', [
        (
            '同期会の開催日は *2020/02/09* です！\n\nannounced: <@ABCDEFG>',
            1581174000
        ),
        (
            '同期会の開催日は *2020/4/8* です！\n\nannounced: <@ABCDEFG>',
            1586271600
        ),
        (
            '同期会の開催日は *2020/11/22* です！\n\nannounced: <@ABCDEFG>',
            1605970800
        ),
    ])
def test_parse_timestamp_for_announce(text, expected):
    actual = app.parse_timestamp_for_announce(text)
    assert expected == actual