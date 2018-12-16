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

python main.py 10min 東京 東京 csv 20181214 20181215
```