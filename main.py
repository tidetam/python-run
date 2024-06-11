import logging
import logging.handlers
import os

import requests
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    #logger.info("Token not available!")
    #raise


if __name__ == "__main__":
    now = datetime.now()
    yesterday = (now - timedelta(days=1)).strftime('%Y-%m-%d')
    district = {
        '天河': '23008636', 
        '越秀': '23008634',
        '荔湾': '23008633',
        '海珠': '23008635',
        '番禺': '23008639',
        '白云': '23008637',
        '黄埔': '23008638',
        '从化': '23008644',
        '增城': '23008643',
        '花都': '23008640',
        '南沙': '23008641',
        '广州': ''
    }
    for k,v in district.items():
        try:
            url = f'https://m.ke.com/archer/api/apiProxy/channelApiProxy/api/index/secondhouse?city_id=440100&ucid=&month=&district_id={v}'
            data = requests.get(url).json()
            cj_cnt = data['data']['data']['supply_index'][0]['num'] # 成交
            xz_cnt = data['data']['data']['supply_index'][1]['num'] # 新增
            dkl_cnt = data['data']['data']['supply_index'][2]['num'] # 带看量
            logger.info(yesterday, k, cj_cnt, xz_cnt, dkl_cnt)
        except Exception as e:
            logger.error(str(e))
