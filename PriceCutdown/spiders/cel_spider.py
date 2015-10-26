__author__ = 'fauri'

from PriceCutdown.items import ProductItem

import scrapy


class CelSpider(scrapy.Spider):
    name = "cel"
    allowed_domains = ["cel.ro"]
    start_urls = ['http://www.cel.ro/laptop-laptopuri/apple/']
    base_product_url = "http://www.cel.ro"

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
            item['product_name'] = content.xpath('//div[@class="pageHeading"]/h2/text()').extract()
            item['product_price'] = content.xpath('//div[@class="pret_info"]/div[@itemprop="offers"]/b/text()').extract()
            item['product_link'] = response.url
            return item