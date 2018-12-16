from pathlib import Path
import pandas as pd
import yaml
import os
from datetime import timedelta, timezone
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


def get_area_ids(prefecture, block):
    fd = Path(__file__).parent
    with open(fd / 'config' / 'area-ids.yaml') as f:
        area_ids_yaml = f.read()
    try:
        area_ids = yaml.load(area_ids_yaml)
    except:
        logger.error('Loading config yaml failed')
    try:
        prec_no = area_ids['Prefecture'][prefecture]['PrefId']
        block_no = area_ids['Prefecture'][prefecture]['Block'][block]['BlockId']
    except:
        logger.error('Parsing config yaml failed')
    logger.debug(f'{prefecture}: {prec_no}, {block}: {block_no}')

    return str(prec_no), str(block_no)
