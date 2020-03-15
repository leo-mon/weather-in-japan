FROM python:3.8

# apt
RUN apt-get update -y && apt-get install -y \
  locales
# User & Group
RUN groupadd -r wij && useradd -r -g wij wij.
# Locale
RUN localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
# Timezone
ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install \
  beautifulsoup4 \
  html5lib \
  ipython \
  lxml \
  pandas \
  pyyaml \
  requests

WORKDIR /wij