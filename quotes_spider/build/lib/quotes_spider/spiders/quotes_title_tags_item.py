# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Response
from scrapy.loader import ItemLoader
from quotes_spider.items import QuotesTitleTagsItemSpiderItem


class QuotesTitleTagsItemSpider(Spider):
    name = 'quotes_title_tags_item'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response: Response):

        l = ItemLoader(item=QuotesTitleTagsItemSpiderItem(), response=response)
        h1 = response.xpath('//h1/a/text()').extract_first()
        tags = response.xpath('//*[@class="tag-item"]/a/text()').extract()
        l.add_value('item_h1_tag', h1)
        l.add_value('item_tags', tags)
        return l.load_item()
