__author__ = 'fauri'

from PriceCutdown.items import ProductItem

import os
import scrapy


class CelSpider(scrapy.Spider):
    name = "cel"
    allowed_domains = ["cel.ro"]
    start_urls = ['http://www.cel.ro/laptop-laptopuri/apple/']
    base_product_url = "http://www.cel.ro"

    def __init__(self, name=None, requests_file='', **kwargs):
        super(CelSpider, self).__init__(name, **kwargs)
        self.requests_file = requests_file

        if os.path.exists(self.requests_file):
            with open(self.requests_file, 'r') as f:
                for line in f:
                    CelSpider.start_urls.append(line.rstrip('\n'))

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        requests_file = crawler.settings.get('CEL_RO_REQUESTS_FILE')
        kwargs['requests_file'] = requests_file
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        return spider

    def parse(self, response):
        item = self.parse_page_content(response)
        if item:
            yield item

        # search for links to follow
        for url in response.xpath('//div[@class="productlisting"]/div[@class="productListing-tot"]/div[@class="productListing-nume"]/h2/a/@href').extract():
            yield scrapy.Request(url, callback=self.parse)

        # search for next page
        for url in response.xpath('//div[@class="pageresults"]/a[text()=">>"]/@href').extract():
            yield scrapy.Request(url, callback=self.parse)

    def parse_page_content(self, response):
        '''
        Parses the response and tries to extract the ProductItem instance
        :return: a ProductItem if found.
        '''
        for content in response.xpath('//div[@class="prod_info"]'):
            item = ProductItem()
            item['product_owner'] = 'cel.ro'
            item['product_name'] = content.xpath('//div[@class="pageHeading"]/h2/text()').extract()[0]
            item['product_price'] = content.xpath('//div[@class="pret_info"]/div[@itemprop="offers"]/b/text()').extract()[0]
            item['product_link'] = response.url
            return item