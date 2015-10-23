__author__ = 'fauri'

from PriceCutdown.items import ProductItem

import scrapy


class EmagSpider(scrapy.Spider):
    name = "emag"
    allowed_domains = ["emag.ro"]
    start_urls = ["http://www.emag.ro/laptopuri/apple/c"]
    base_product_url = "http://www.emag.ro"

    def parse(self, response):
        item = self.parse_page_content(response)
        if item:
            yield item

        # search for links to follow
        for url in response.xpath('//form/h2/a/@href').extract():
            yield scrapy.Request(response.urljoin(url), callback=self.parse)


    def parse_page_content(self, response):
        '''
        Parses the response and tries to extract the EmagItem instance
        :return: a EmagInstance if found.
        '''
        for content in response.xpath('//div[@class="big-box" and @itemprop="offerDetails"]'):
            item = ProductItem()
            item['product_owner'] = 'emag.ro'
            item['product_name'] = content.xpath('//div[@id="product-offer"]/div[@id="offer-title"]/h1/text()').extract()
            item['product_price'] = content.xpath('//span[@itemprop="price" and @content]/@content').extract()
            item['product_link'] = response.url
            return item