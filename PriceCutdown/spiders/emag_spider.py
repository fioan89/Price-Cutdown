__author__ = 'fauri'

import scrapy
import urlparse


class EmagSpider(scrapy.Spider):
    name = "emag"
    allowed_domains = ["emag.ro"]
    start_urls = ["http://www.emag.ro/laptopuri/apple/c"]
    base_product_url = "http://www.emag.ro"

    def parse(self, response):
        for url in response.xpath('//form/h2/a/@href').extract():
            yield scrapy.Request(urlparse.urljoin(self.base_product_url, url), callback=self.parse)
