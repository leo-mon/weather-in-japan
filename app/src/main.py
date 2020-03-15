from pathlib import Path
import pandas as pd
import yaml
import os
from datetime import datetime, timedelta, timezone
import locale
import time
import argparse
from logging import getLogger, StreamHandler, Formatter
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))  # TODO: move to __init__
from src.scraper import fetch_weather_by_10, fetch_hourly_weather
from src.yaml_config_parser import get_area_ids, get_all_dict

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

def main(sampling_rate, prefecture, block, format, start_date, end_date):
    start_datetime = datetime.strptime(start_date, '%Y%m%d')
    end_datetime = datetime.strptime(end_date, '%Y%m%d')
    if prefecture != 'all':
        prec_no, block_no = get_area_ids(prefecture, block)
        output_dir = Path(__file__).parent.parent / 'output' / sampling_rate / prec_no / block_no
        output_dir.mkdir(parents=True, exist_ok=True)
        i = start_datetime  # Not necessary but for understanding
        if sampling_rate == '10min':
            while i <= end_datetime:
                logger.info(f'Fetching: {i}')
                df = fetch_weather_by_10(prec_no, block_no, i.year, i.month, i.day)
                if format == 'csv':
                    filename = f'{i.strftime("%Y%m%d")}.csv'
                    df.to_csv(output_dir/filename, index=False)
                    logger.info(f'Saved: {output_dir/filename}')
                time.sleep(1)  # Not to heavy load onto the server
                i += timedelta(days=1)
        elif sampling_rate == 'hourly':
            while i <= end_datetime:
                logger.info(f'Fetching: {i}')
                df = fetch_hourly_weather(prec_no, block_no, i.year, i.month, i.day)
                if format == 'csv':
                    filename = f'{i.strftime("%Y%m%d")}.csv'
                    df.to_csv(output_dir/filename, index=False)
                    logger.info(f'Saved: {output_dir / filename}')
                time.sleep(1)  # Not to heavy load onto the server
                i += timedelta(days=1)
    else:
        area_ids = get_all_dict()
        logger.debug(area_ids)
        for prec in area_ids['Prefecture'].keys():
            prec_no = area_ids['Prefecture'][prec]['PrefId']
            for block in area_ids['Prefecture'][prec]['Block'].keys():
                block_no = area_ids['Prefecture'][prec]['Block'][block]['BlockId']
                logger.info(f'Target: {prec}/{block}({prec_no}/{block_no})')
                output_dir = Path(__file__).parent.parent / 'output' / sampling_rate / prec_no / block_no
                output_dir.mkdir(parents=True, exist_ok=True)
                i = start_datetime  # Not necessary but for understanding
                if sampling_rate == '10min':
                    while i <= end_datetime:
                        logger.info(f'Fetching: {i}')
                        df = fetch_weather_by_10(prec_no, block_no, i.year, i.month, i.day)
                        if format == 'csv':
                            filename = f'{i.strftime("%Y%m%d")}.csv'
                            df.to_csv(output_dir/filename, index=False)
                            logger.info(f'Saved: {output_dir/filename}')
                        time.sleep(1)  # Not to heavy load onto the server
                        i += timedelta(days=1)

    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sequently save weather data')
    parser.add_argument('sampling_rate', help='Sampling rate, e.g. 10min or hourly')
    parser.add_argument('prefecture', help='Prefecture, e.g. 東京')
    parser.add_argument('block', help='Block, e.g. 東京')
    parser.add_argument('format', help='Format, csv')
    parser.add_argument('start_date', help='Start point, e.g. 20181214')
    parser.add_argument('end_date', help='End point, e.g. 20181215')

    args = parser.parse_args()

    main(args.sampling_rate, args.prefecture, args.block, args.format, args.start_date, args. end_date)