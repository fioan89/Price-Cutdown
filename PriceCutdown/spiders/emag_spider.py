__author__ = 'fauri'

from PriceCutdown.items import ProductItem

import os
import scrapy


class EmagSpider(scrapy.Spider):
    name = "emag"
    allowed_domains = ["emag.ro"]
    start_urls = ["http://emag.ro/laptopuri/apple/c"]
    base_product_url = "http://emag.ro"

    def __init__(self, name=None, requests_file='', **kwargs):
        super(EmagSpider, self).__init__(name, **kwargs)
        self.requests_file = requests_file

        if os.path.exists(self.requests_file):
            with open(self.requests_file, 'r') as f:
                for line in f:
                    EmagSpider.start_urls.append(line.rstrip('\n'))

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        requests_file = crawler.settings.get('EMAG_RO_REQUESTS_FILE')
        kwargs['requests_file'] = requests_file
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        return spider

    def parse(self, response):
        item = self.parse_page_content(response)
        if item:
            yield item

        # search for links to follow
        for url in response.xpath('//form/h2/a/@href').extract():
            yield scrapy.Request(response.urljoin(url), callback=self.parse)

    def parse_page_content(self, response):
        '''
        Parses the response and tries to extract the ProductItem instance
        :return: a ProductItem if found.
        '''
        for content in response.xpath('//div[@class="big-box" and @itemprop="offerDetails"]'):
            item = ProductItem()
            item['product_owner'] = 'emag.ro'
            item['product_name'] = content.xpath('//div[@id="product-offer"]/div[@id="offer-title"]/h1/text()').extract()[0]
            item['product_price'] = content.xpath('//span[@itemprop="price" and @content]/@content').extract()[0]
            item['product_link'] = response.url
            return item
