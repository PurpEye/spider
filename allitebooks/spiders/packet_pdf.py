from allitebooks.items import PacketstormsItem
from scrapy import Spider, Item, Field, Request
import urllib
import urlparse
import re
import validators

class MySpider(Spider):
    name = "packetstorm_collector"
    allowed_domains = ["packetstormsecurity.com"]
    start_urls = ["https://packetstormsecurity.com"]
 
    def parse(self, response):
        links = response.xpath('//a/@href').extract()
        base_url='https://packetstormsecurity.com/'

        if response.url.endswith('.html'): 
            for sel in response.xpath('//dl[contains(class,"File First")]'):
                item = PacketstormsItem()
                item['link'] = response.url
                item['title'] = sel.xpath('//dt/a/strong/text()').extract()
                item['author'] = sel.xpath('//dd[contains(class,"refer")/a/text()').extract()
                item['date'] = sel.xpath('//dd[contains(class,"datetime")/a/text()').extract()
                item['detail'] = sel.xpath('//dd[contains(class,"detail")/p/text()').extract()
                item['tags'] = sel.xpath('//dd[contains(class,"tags")/a/text()').extract()
                print "[*]record:"+response.url
                yield item

        for i in links:
            #if "https://dl" in i:
            #    if i.endswith('.pdf'):
            #        print "[****]Now download!"+i
            #        yield AllitebooksItem(link=i)
            #        #yield Request(i, callback=self.save_pdf)
            #    print "[abandon]"+i
            #else:
            #if i.endswith('.html'):
            #    if "download" in i:
            #        i = urlparse.urljoin(base_url, i)
            #        print "[retry]"+i
            #        yield Request(i)
            #        continue
            if not validators.url(i):
                i = urlparse.urljoin(base_url, i)
            #if "exploit" in i:
            #    continue
            #if "advisory" in i:
            #    continue
            if "news" in i:
                continue
            if "tool" in i:
                continue
            if "author" in i:
                continue
            if "https://dl" in i:
                continue         
            if "files/download" in i:
                continue      
            yield Request(i)
        
    def save_pdf(self, response):
        print "[**************]"
        print "download link:"+response.url
        print "[**************]"
        path = response.url.split('/')[-1]
        path = urllib.unquote(path)
        path = "./resources/packetstorm/" + path
        with open(path, 'wb') as f:
            f.write(response.body)   
        
