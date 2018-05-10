import requests

url="http://www.dianping.com/search/keyword/8/0_%E5%A4%A9%E5%BA%9C%E4%B8%89%E8%A1%97%E7%BE%8E%E9%A3%9F"

response = requests.get(url)

contents_li = response.xpath("//div[@id='shop-all-list']/ul/li")
for li in contents_li:
    name = li.xpath("./div[@class='txt']/div[@class='tit']/a/h4/text()").extract()[0].strip()
    print(name)