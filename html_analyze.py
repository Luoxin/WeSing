# coding:utf-8
import json

from bs4 import BeautifulSoup
import re
from urllib import parse

class HtmlParser(object):
    def parse(self,html_content):
        # print("正在分析页面....")

        soup = BeautifulSoup(html_content, 'lxml')
        singer = soup.select('.singer_user__name')[0]
        music_name = soup.select('.play_name')[0].text.strip()
        r_data = soup.select('script')[2].text[18:-2]
        singer_name = singer.text.strip()
        audio_url = json.loads(r_data)['detail']['playurl']
        return {"audio_url":audio_url,"singer_name":singer_name,"music_name":music_name}
