import os
import time
import codecs
from collections import OrderedDict
import requests
import yaml
from urllib.parse import parse_qs
from bs4 import BeautifulSoup
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
YAML setting
"""


def represent_ordereddict(dumper, data):
    value = []

    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)


yaml.add_representer(OrderedDict, represent_ordereddict)


"""
Prefecture
"""
base_url = 'https://www.data.jma.go.jp/obd/stats/etrn/select/prefecture00.php'

base_html = requests.get(base_url)
logger.debug(base_html.text)

base_soup = BeautifulSoup(base_html.content, 'lxml')
prefectures = base_soup.find('div', {'id': 'main'}).find_all('area')
ids_dict = OrderedDict()
ids_dict.setdefault('Prefecture', {})
for prec in prefectures:
    prec_name = prec['alt']
    logger.debug(prec_name)
    prec_no = parse_qs(prec['href'])['prefecture.php?prec_no'][0]
    logger.debug(prec_no)
    ids_dict['Prefecture'].setdefault(prec_name, {'PrefId': prec_no})
    ids_dict['Prefecture'][prec_name]['Block'] = {}
    ids_dict['Prefecture'] = OrderedDict(sorted(ids_dict['Prefecture'].items(), key=lambda x:x[1]['PrefId']))
    logger.debug(ids_dict)

    """
    Block
    """
    prec_url = f'https://www.data.jma.go.jp/obd/stats/etrn/select/prefecture.php?prec_no={prec_no}'
    prec_html = requests.get(prec_url)
    logger.debug(prec_html.text)

    prec_soup = BeautifulSoup(prec_html.content, 'lxml')
    blocks = prec_soup.find('div', {'id': 'contents_area2'}).find_all('area')
    logger.debug(blocks)
    logger.debug(ids_dict)

    #if prec_no != '44':
    #    continue
    for block in blocks:
        block_name = block['alt']
        logger.debug(block_name)
        try:
            block_no = str(parse_qs(block['href'])['block_no'][0])
            logger.debug(block_no)
            ids_dict['Prefecture'][prec_name]['Block'][block_name] = {'BlockId': block_no}
        except KeyError as e:
            logger.warning(f"KeyError about: {block['alt']}")
    ids_dict['Prefecture'][prec_name]['Block'] = OrderedDict(sorted(ids_dict['Prefecture'][prec_name]['Block'].items(),
                                                                    key=lambda x:x[1]['BlockId']))

    time.sleep(1)
logger.debug(ids_dict)
logger.debug(ids_dict['Prefecture']['東京都']['Block']['調布'])
logger.debug(ids_dict['Prefecture']['東京都']['Block']['世田谷'])

with codecs.open('area-ids.yaml', 'w', 'utf-8') as f:
    yaml.dump(ids_dict, f, encoding='utf-8', allow_unicode=True)


