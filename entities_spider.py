#__author: Joey
#date:    2018/6/11
import requests
#网页下载
class HtmlDownloader(object):
    def download(self,url):
        if url is None:
            return None
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        r = requests.get(url,headers=headers)
        if r.status_code == 200:
            r.encoding='utf-8'
            return r.text
        return None
#网页解析
import re
from bs4 import BeautifulSoup
class HtmlParser(object):
    def parser(self,page_url,html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont,'html.parser')
        urls = self.get_new_urls(soup)
        data = self.get_new_data(page_url,soup)
        return urls,data
    def get_new_urls(self,soup):
        new_urls = set()
        urls = soup.find_all('a',href=re.compile(r'^/item/'))
        for i in urls:
            url = 'https://baike.baidu.com'+i['href']
            new_urls.add(url)
        return new_urls
    def get_new_data(self,page_url,soup):
        data = {}
        data['url'] = page_url
        data['title'] = re.search('(.*?)_百度百科',soup.title.string).group(1)
        data['content'] = soup.find(attrs={'name':"description"})['content']
        return data



















