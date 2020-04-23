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
