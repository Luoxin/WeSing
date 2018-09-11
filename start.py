import json
import os
from time import sleep
import  sys

from bs4 import BeautifulSoup
from selenium import webdriver
import tqdm

from url_controller import UrlControl
from download_html import HtmlDownloader
from html_analyze import HtmlParser
from download_file import download_file


class WeSong():
    def __init__(self):
        self.downloadHTML=HtmlDownloader()  # 用于下载列表页
        self.songPageParse=HtmlParser()  # 用于解析歌曲页

        self.songPage=UrlControl()  # 歌曲页
        self.downloadMusic=UrlControl()  # 下载连接以及下载的相关信息

        self.driver_name = 'chrome'
        self.executable_path = "./chromedriver.exe"  # 驱动
        # self.driver = webdriver.PhantomJS()


        # 基础信息
        self.baseURL="http://kg.qq.com/node/personal?uid="  # 歌手主页
        # self.path="F:/Song/"
        self.path="F:/Song/"  # 存储位置

        try:
            os.mkdir(self.path)
        except:
            pass


    def get_songPageUrl(self,url):
        '''
        1. 通过click点击事件展开被隐藏页
        2. 获取歌曲详情页的地址
        :param url:
        :return:
        '''
        self.driver.get(url)
        count_SongMore = self.driver.find_elements_by_xpath('//div[@class="mod_more"]/a').__len__()
        for i in range(count_SongMore + 2):
            try:
                if not self.driver.find_elements_by_xpath('//div[@class="mod_more"]/a[@style="display: none"]'):
                    self.driver.find_elements_by_xpath('//div[@class="mod_more"]/a')[0].click()
                sleep(2)
            except:
                pass


        try:
            addurl_objs = self.driver.find_elements_by_xpath('//ul//li[@class="mod_playlist__item"]//a')

            for i,addurl_obj in enumerate(addurl_objs):
                self.songPage.add_new_url(addurl_obj.get_attribute("href"))
        except:
            pass



    def main(self,ids):
        '''
        1. 下载页面
        2. 页面解析
        3. 扩链以（歌曲也以及下载连接）
        4. 调用下载器下载歌曲
        :return:
        '''


        urls =[]
        for id in ids:
            # urls.append(self.baseURL+id)
            urls.append(id)

        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1200, 800)
        for url in urls:
            try:
                self.get_songPageUrl(url)
            except:
                pass
        self.driver.close()
        self.driver.__exit__()

        print(f"获取到{self.songPage.get_urls_len()}个歌曲")

        # url="http://node.kg.qq.com/play?s=zSl-ohzGH3_1Uz1W&g_f=personal"
        while self.songPage.has_new_url():
            try:
                url=self.songPage.get_new_url()
                songPage_html=self.downloadHTML.download(url)
                musicInfo=self.songPageParse.parse(songPage_html)
                self.downloadMusic.add_new_url(json.dumps(musicInfo))
                sleep(2)
            except:
                pass


        print(f"获得{self.downloadMusic.get_urls_len()}个下载连接")

        while self.downloadMusic.has_new_url():
            try:
                itme=json.loads(self.downloadMusic.get_new_url())
                url=itme["audio_url"]
                fileName=self.path+str(itme["singer_name"])+"-"+str(itme["music_name"])+".m4a"
                download_file(url,fileName)
            except:
                pass

        print("End")


if __name__ == '__main__':
    w=WeSong()
    try:
        ids=list(sys.argv[1:])
        print(ids)
    except:
        ids =["http://kg.qq.com/node/personal?uid=619a958c25283e88"]  # 存放歌手首页地址
    w.main(ids)
