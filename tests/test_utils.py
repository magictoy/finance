import os
import types

import pytest

from finance.utils import (
    date_range, extract_numbers, make_date, parse_8percent_data)


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_PATH = os.path.abspath(os.path.join(BASE_PATH, '..'))


def test_date_range():
    start, end = make_date('2016-01-01'), make_date('2016-01-15')
    r = date_range(start, end)
    assert isinstance(r, types.GeneratorType)

    r = list(r)
    assert 14 == len(r)
    assert r[0] == make_date('2016-01-01')
    assert r[13] == make_date('2016-01-14')


def test_extract_numbers():
    assert '160' == extract_numbers('160')
    assert '1694' == extract_numbers('1,694')
    assert '1806' == extract_numbers('1,806 원')

    assert 170 == extract_numbers('170', int)
    assert 3925321 == extract_numbers('3,925,321', int)

    assert 150.25 == extract_numbers('150.25', float)


def test_parse_8percent_data():
    sample_file = os.path.join(PROJECT_PATH, 'sample-data',
                               '8percent-829.html')
    with open(sample_file) as fin:
        raw = fin.read()

    stored_data = [
        ('2016-04-11', 1694, 612, 160, 340),
        ('2016-05-11', 1916, 390, 90, 0),
        ('2016-06-13', 1920, 386, 90, 0),
        ('2016-07-11', 1982, 324, 80, 0),
        ('2016-08-10', 1963, 343, 80, 0),
        ('2016-09-12', 1979, 327, 80, 0),
        ('2016-10-10', 2005, 301, 70, 0),
        ('2016-11-14', 1992, 314, 70, 0),
        ('2016-12-12', 2054, 252, 60, 0),
        ('2017-01-10', 2044, 262, 60, 0),
        ('2017-02-13', 2053, 253, 60, 0),
        ('2017-03-13', 2099, 207, 50, 0),
        ('2017-04-10', 2101, 205, 50, 0),
        ('2017-05-15', 2098, 208, 50, 0),
        ('2017-06-12', 2145, 161, 40, 0),
        ('2017-07-10', 2151, 155, 30, 0),
        ('2017-08-14', 2153, 153, 30, 0),
        ('2017-09-11', 2188, 118, 20, 0),
        ('2017-10-11', 2198, 108, 20, 0),
        ('2017-11-13', 2216, 90, 20, 0),
        ('2017-12-11', 2238, 68, 10, 0),
        ('2018-01-10', 2251, 55, 10, 0),
        ('2018-02-12', 2270, 36, 0, 0),
        ('2018-03-12', 2290, 16, 0, 0),
    ]

    parsed_data = parse_8percent_data(raw)

    assert parsed_data['name']
    assert parsed_data['grade']
    assert isinstance(parsed_data['duration'], int)
    assert isinstance(parsed_data['annual_percentage_yield'], float)
    assert 0.0 < parsed_data['annual_percentage_yield'] <= 0.3
    assert isinstance(parsed_data['amount'], int)
    assert 0 < parsed_data['amount']

    flag = True
    for expected, actual in zip(stored_data, parsed_data['records']):
        assert len(expected) == len(actual)
        expected = list(expected)
        expected[0] = make_date(expected[0])
        for exp, act in zip(expected, actual):
            flag = False
            assert exp == act

    if flag:
        pytest.fail('parse_8percent_data() did not return any data')
