from allitebooks.items import AllitebooksItem
from scrapy import Spider, Item, Field, Request
import urlparse
import re
import validators

class MySpider(Spider):
  name = "allitebooks_collector"
  allowed_domains = ["allitebooks.com"]
  start_urls = ["http://www.allitebooks.com/"]
 
  def parse(self, response):
    links = response.xpath('//a/@href').extract()
    base_url='http://file.allitebooks.com/'
    for i in links:
      if i.endswith('.pdf'):
        i = urlparse.urljoin(base_url, i)
        print "[*]request book:"+i
        yield Request(i, callback=self.save_pdf)
    yield AllitebooksItem(link=response.url)
    for link in links:
      if validators.url(link):
        yield Request(link)
        
  def save_pdf(self, response):
    path = response.url.split('/')[-1]
    path = urllib.unquote(path)
    print "[**]saving book:"+path
    path = "./resources/packetstorm/" + path
    with open(path, 'wb') as f:
      f.write(response.body)   
