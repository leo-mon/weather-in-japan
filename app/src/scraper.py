from pathlib import Path
import pandas as pd
import yaml
import os
from datetime import datetime, timedelta, timezone
import locale
from logging import getLogger, StreamHandler, Formatter

"""
Log setting
"""
# root logger
logger = getLogger(__name__)
logger.setLevel(os.getenv('LOG_LEVEL', 'WARNING'))
# log format
formatter = Formatter('[%(asctime)s] %(module)s.%(funcName)s %(levelname)s -> %(message)s')
# handler
ch = StreamHandler()  # handler for stderr output
ch.setLevel(os.getenv('LOG_LEVEL', 'WARNING'))
ch.setFormatter(formatter)
# binding
logger.addHandler(ch)
logger.propagate = False  # Not propagate to the upper component

"""
Locale setting
"""
locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')

"""
TZ setting
"""
JST = timezone(timedelta(hours=+9), 'JST')


def construct_url(sampling_rate, prec_no, block_no, year, month, day):
    base_url = f'https://www.data.jma.go.jp/obd/stats/etrn/view/{sampling_rate}_s1.php'
    url = f'{base_url}?prec_no={prec_no}&block_no={block_no}&year={year}&month={month}&day={day}&view=p1'
    logger.info(f'Target: {url}')
    return url


def fetch_weather_by_10(prec_no, block_no, year, month, day):
    url = construct_url('10min', prec_no, block_no, year, month, day)
    df = pd.read_html(url, skiprows=2)[0]
    df.columns = [
        'timestamp',
        'local_atm',
        'sea_level_atm',
        'precipitation',
        'temperature',
        'relative_humidity',
        'ave_wind_speed',
        'wind_direction_ave',
        'max_wind_speed',
        'wind_direction_max',
        'sunshine_duration'
    ]
    df.timestamp = f'{year}/{month}/{day} ' + df.timestamp
    df.timestamp.values[-1] = datetime.strptime(f'{year}{month}{day}','%Y%m%d') + timedelta(days=1)
    df.timestamp = pd.to_datetime(df.timestamp).dt.tz_localize('Asia/Tokyo')
    logger.debug(df)
    return df


def fetch_hourly_weather(prec_no, block_no, year, month, day):
    url = construct_url('hourly', prec_no, block_no, year, month, day)
    df = pd.read_html(url, skiprows=2)[0]
    df.columns = [
        'timestamp',
        'local_atm',
        'sea_level_atm',
        'precipitation',
        'temperature',
        'dew_point',
        'vapor_pressure',
        'humidity',
        'wind_speed',
        'wind_direction',
        'sunshine_duration',
        'total_solar_radiation',
        'snowfall',
        'snow_depth',
        'weather',
        'cloudiness',
        'visibility',
    ]
    df.timestamp = f'{year}/{month}/{day} ' + df.timestamp.astype('str') + ':00'
    df.timestamp.values[-1] = datetime.strptime(f'{year}{month}{day}','%Y%m%d') + timedelta(days=1)
    df.timestamp = pd.to_datetime(df.timestamp).dt.tz_localize('Asia/Tokyo')
    logger.debug(df)
    return df
