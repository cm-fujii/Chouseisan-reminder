import json

import pytest

from datetime import date
from src.notify_1st_message import app

@pytest.mark.parametrize(
    'base, target, expected', [
        (date(2019, 1, 1), date(2019, 3, 1), 1),
        (date(2019, 1, 1), date(2019, 4, 1), 2),
        (date(2019, 1, 1), date(2019, 5, 1), 3),
        (date(2019, 1, 1), date(2019, 6, 1), 4),
        (date(2019, 1, 1), date(2019, 7, 1), 5),
        (date(2019, 1, 1), date(2019, 8, 1), 6),
        (date(2019, 1, 1), date(2019, 9, 1), 7),
        (date(2019, 1, 1), date(2019, 10, 1), 8),
        (date(2019, 1, 1), date(2019, 11, 1), 9),
        (date(2019, 1, 1), date(2019, 12, 1), 10),
    ])
def test_get_vol(base, target, expected):
    actual = app.get_vol(base, target)
    assert expected == actual

@pytest.mark.parametrize(
    'target_date, expected', [
        (date(2019, 12, 1), False),
        (date(2019, 12, 2), True),
        (date(2019, 12, 3), False),
        (date(2019, 12, 4), False),
        (date(2019, 12, 5), False),
        (date(2019, 12, 6), False),
        (date(2019, 12, 7), False),

        (date(2020, 1, 1), False),
        (date(2020, 1, 2), True),
        (date(2020, 1, 3), False),
        (date(2020, 1, 4), False),
        (date(2020, 1, 5), False),
        (date(2020, 1, 6), False),
        (date(2020, 1, 7), False),

        (date(2020, 2, 1), False),
        (date(2020, 2, 2), False),
        (date(2020, 2, 3), True),
        (date(2020, 2, 4), False),
        (date(2020, 2, 5), False),
        (date(2020, 2, 6), False),
        (date(2020, 2, 7), False),

        (date(2020, 3, 1), False),
        (date(2020, 3, 2), True),
        (date(2020, 3, 3), False),
        (date(2020, 3, 4), False),
        (date(2020, 3, 5), False),
        (date(2020, 3, 6), False),
        (date(2020, 3, 7), False),

        (date(2020, 5, 1), True),
        (date(2020, 5, 2), False),
        (date(2020, 5, 3), False),
        (date(2020, 5, 4), False),
        (date(2020, 5, 5), False),
        (date(2020, 5, 6), False),
        (date(2020, 5, 7), False),

        (date(2020, 11, 1), False),
        (date(2020, 11, 2), True),
        (date(2020, 11, 3), False),
        (date(2020, 11, 4), False),
        (date(2020, 11, 5), False),
        (date(2020, 11, 6), False),
        (date(2020, 11, 7), False),

        (date(2021, 5, 1), False),
        (date(2021, 5, 2), False),
        (date(2021, 5, 3), False),
        (date(2021, 5, 4), False),
        (date(2021, 5, 5), False),
        (date(2021, 5, 6), True),
        (date(2021, 5, 7), False),
    ])
def test_is_notify(target_date, expected):
    actual = app.is_first_working_day(target_date)
    assert expected == actual
