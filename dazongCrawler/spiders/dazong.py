# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from dazongCrawler.items import DazongcrawlerItem
import pdb
import time
from scrapy.spidermiddlewares.httperror import  HttpError
from twisted.internet.error import ConnectionLost
from twisted.internet.error import ConnectError
from twisted.internet.error import DNSLookupError
#https://www.cnblogs.com/wzjbg/p/6507581.html 设置代理, proxy configuration
class DazongSpider(scrapy.Spider):
    name = 'dazong'
    allowed_domains = ['www.dianping.com']
    url="http://www.dianping.com/search/keyword/8/0_%E5%A4%A9%E5%BA%9C%E4%B8%89%E8%A1%97%E7%BE%8E%E9%A3%9F/{}"
    start_urls = [url.format('p1')]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse, errback=self.errorhandel)

    def parse(self, response):
        pdb.set_trace()
        contents_li = response.xpath("//div[@id='shop-all-list']/ul/li")
        print("******!!!!!!",response.status)
        # for li in contents_li:
        #     item =self.generat_items(li)
        #     yield item

        # next_page_url = response.xpath("//div[@class='page']/a[@class='next']/@href").extract()[0].strip()
        # print("Next Page******",next_page_url)
        # if(next_page_url!=None):
        #     yield scrapy.Request(next_page_url,callback=self.parse_nextPage)

        offset=2
        while(offset<5):
            offpage = 'p'+str(offset)
            next_page_url=self.url.format(offpage)
            print("Next Page******",next_page_url)
            offset += 1
            time.sleep(10)
            yield scrapy.Request(next_page_url, callback=self.parse_nextPage,errback=self.errorhandel)

    def parse_nextPage(self, response):
        contents_li = response.xpath("//div[@id='shop-all-list']/ul/li")
        for li in contents_li:
            item = self.generat_items(li)
            yield item

    def errorhandel(self,failure):
        # pdb.set_trace()
        if failure.check(HttpError):
            response = failure.value.response
            print("http error Url:", response.url)
        elif failure.check(ConnectError):
            print("connect error:",failure)
        elif failure.check(DNSLookupError):
            print("dns:",failure)

            


    def generat_items(self,li):
        item = DazongcrawlerItem()
        pdb.set_trace()
        # shopObj = li.xpath("./div[@class='txt']/div[@class='tit']")
        name = li.xpath("./div[@class='txt']/div[@class='tit']/a/h4/text()").extract()[0].strip()
        # storeStar =shopObj.xpath("./div[@class='comment']")
        tag = li.xpath("./div[@class='txt']/div[@class='tag-addr']/a[1]/span/text()").extract()[0].strip()
        location = li.xpath("./div[@class='txt']/div[@class='tag-addr']/span/text()").extract()[0].strip()
        price_node = li.xpath("./div[@class='txt']/div[@class='comment']/a[@class='mean-price']/b/text()")
        mean_price = ""
        if(len(price_node)>0):
            mean_price = li.xpath("./div[@class='txt']/div[@class='comment']/a[@class='mean-price']/b/text()")[0].extract().strip()

        item["name"] = name
        item["tag"] = tag
        item["location"] = location
        item["meanPrice"] =mean_price
        return item