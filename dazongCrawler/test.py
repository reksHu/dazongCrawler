import requests
from lxml import etree
url="http://www.dianping.com/search/keyword/8/0_%E5%A4%A9%E5%BA%9C%E4%B8%89%E8%A1%97%E7%BE%8E%E9%A3%9F"
headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
           'Accept - Encoding': 'Accept-Encoding	gzip, deflate',
           'Accept-Language': 'en-US',
           'Connection': 'Keep-Alive',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}

response = requests.get(url,headers = headers)
tree = etree.HTML(response.text)
contents_li = tree.xpath("//div[@id='shop-all-list']/ul/li")
for li in contents_li:
    name = li.xpath("./div[@class='txt']/div[@class='tit']/a/h4/text()").extract()[0].strip()
    print(name)