# Weather in Japan
試験用の天気データを気象庁サイトより取得

- 気象庁 各種データ・資料: https://www.jma.go.jp/jma/menu/menureport.html

## script


```bash
docker build -t wij:dev -f Dev.Dockerfile .

docker run -it --rm\
  -v $(pwd)/app:/wij \
  -e LOG_LEVEL=DEBUG \
  wij:dev \
  /bin/bash

python -m unittest discover
python -m unittest tests.test_scraper.TestScraper

python src/main.py 10min 東京都 東京 csv 20200310 20200311
python src/main.py 10min 神奈川県 横浜 csv 20200310 20200311
python src/main.py 10min all all csv 20200310 20200310

```