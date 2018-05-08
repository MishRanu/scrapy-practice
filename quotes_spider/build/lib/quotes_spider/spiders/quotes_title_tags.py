# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Response


class QuotesTitleTagsSpider(Spider):
    name = 'quotes_title_tags'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response: Response):
        h1 = response.xpath('//h1/a/text()').extract_first()
        tags = response.xpath('//*[@class="tag-item"]/a/text()').extract()

        yield {
            'H1': h1,
            "Tags": tags
        }