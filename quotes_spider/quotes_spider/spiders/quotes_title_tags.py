# -*- coding: utf-8 -*-
from scrapy import Spider


class QuotesTitleTagsSpider(Spider):
    name = 'quotes_title_tags'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        h1 = response.xpath('//h1/a/text()').extract_first()
        tags = response.xpath('//*[@class="tag-item"]/a/text()').extract()

        yield {
            'H1': h1,
            "Tags": tags
        }