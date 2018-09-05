import json
import os
from time import sleep
from contextlib import closing
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import tqdm

from url_controller import UrlControl
from download_html import HtmlDownloader
from html_analyze import HtmlParser


class WeSong():
    def __init__(self):
        self.downloadHTML=HtmlDownloader()
        self.songPageParse=HtmlParser()

        self.songPage=UrlControl()
        self.downloadMusic=UrlControl()

        self.driver_name = 'chrome'
        self.executable_path = "./chromedriver.exe"
        # self.driver = webdriver.PhantomJS()


        # 基础信息
        self.baseURL="http://kg.qq.com/node/personal?uid="
        self.path="F:/Song"

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
            # break

        try:
            addurl_objs = self.driver.find_elements_by_xpath('//ul//li[@class="mod_playlist__item"]//a')

            for i,addurl_obj in enumerate(addurl_objs):
                self.songPage.add_new_url(addurl_obj.get_attribute("href"))
        except:
            pass

    def download_file(self,url,fileName):
        with closing(requests.get(url, stream=True)) as response:
            chunk_size = 1024  # 单次请求最大值
            content_size = int(response.headers['content-length'])  # 内容体总大小
            data_count = 0
            with open(fileName, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    data_count = data_count + len(data)
                    now_jd = (data_count / content_size) * 100
                    # print("\r %s文件下载进度：%d%%(%d/%d) - %s" % (fileName,now_jd, data_count, content_size, url), end=" ")
                    print(f"\r \t{fileName} \t下载进度 \t{now_jd}%( {data_count/1024}kb/{content_size/1024}kb )\t", end="")


    def main(self,ids):
        '''
        1. 下载页面
        2. 页面解析
        3. 扩链以（歌曲也以及下载连接）
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
            # break

        print(f"获得{self.downloadMusic.get_urls_len()}个下载连接")

        while self.downloadMusic.has_new_url():
            try:
                itme=json.loads(self.downloadMusic.get_new_url())
                url=itme["audio_url"]
                fileName=self.path+str(itme["singer_name"])+"-"+str(itme["music_name"])+".m4a"
                self.download_file(url,fileName)
                print(f'{itme["singer_name"]}-{itme["music_name"]} 下载完成')
                #sleep(2)
            except:
                pass

        print("End")

        pass



if __name__ == '__main__':
    w=WeSong()
    ids =["http://kg.qq.com/node/personal?uid=619a958c25283e88"]  # 存放歌手首页地址
    w.main(ids)
