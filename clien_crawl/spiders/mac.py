import scrapy
import requests
from bs4 import BeautifulSoup
import urllib.parse as urlparse
from clien_crawl.items import Article
from pymongo import MongoClient 
import datetime
import sys
import PyRSS2Gen



class MacSpider(scrapy.Spider):
    name = 'mac'
    allowed_domains = ['clien.net']
    start_urls = ['https://www.clien.net/service/board/cm_mac']
    base_url = 'https://www.clien.net'
    request_header = {
        "Accept": "*/*",
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac Os X 10_9_5) AppleWebKit 537.36 (KHMTL, like Gecko) Chrome',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4'
    }

    def parse(self, response):
        meta = dict()
        for i in range(3,-1,-1):
            if i == 0: 
                print(self.start_urls[0])
                try:
                    r = requests.get(self.start_urls[0])
                    bs_obj = BeautifulSoup(r.text, 'lxml')
                    links = bs_obj.findAll('div', {'class' : 'list_item symph_row'})
                    for link in links:
                        article_url = link.find('a')['href']
                        article_title = link.a.find('span', {'data-role' : 'list-title-text'}).attrs['title']
                        meta['article_title'] = article_title
                        meta['article_url'] = urlparse.urljoin(self.base_url, article_url)
                        yield scrapy.Request(
                            urlparse.urljoin(self.base_url, article_url), 
                            callback=self.parse_articles,
                            headers=self.request_header,
                            meta=meta
                            )    
                except:
                    continue

            else:
                # print u + '&po=%d' % i
                try:
                    r = requests.get(self.start_urls[0] + '?&po=%d' % i)
                    bs_obj = BeautifulSoup(r.text, 'lxml')
                    links = bs_obj.findAll('div', {'class' : 'list_item symph_row'})
                    for link in links:
                        article_url = link.find('a')['href']
                        article_title = link.a.find('span', {'data-role' : 'list-title-text'}).attrs['title']
                        meta['article_title'] = article_title
                        meta['article_url'] = urlparse.urljoin(self.base_url, article_url)
                        yield scrapy.Request(
                            urlparse.urljoin(self.base_url, article_url), 
                            callback=self.parse_articles,
                            headers=self.request_header,
                            meta=meta
                            )
                except:
                    continue
                     
    def parse_articles(self, response):
        meta = response.meta.copy()
        item = Article()
        bs_obj = BeautifulSoup(response.text, 'lxml')
        
        client = MongoClient('localhost', 27017)
        db = client.scrap_clien

        item['title'] = meta['article_title']
        item['body'] = bs_obj.find('div', {'class' : 'post_article fr-view'}).text # or .get_text()
        item['url'] = meta['article_url']

        collection = db.article
        collection.insert_one({'title': item['title'], 'body': item['body'], 'url': item['url']})     

        yield item 

