# -*- coding: utf-8 -*-
import scrapy


class PopRankSpider(scrapy.Spider):
    name = 'pop_rank'
    allowed_domains = ['http://en.wikipedia.org']
    start_urls = ['http://en.wikipedia.org/wiki/List_of_United_States_cities_by_population']

    def parse(self, response):
        table = response.xpath('//table[@class="wikitable sortable"]')[0]
        for row in table.xpath('.//tr')[1:]:
            rank = row.xpath('.//td[1]/text()').extract_first()
            city = row.xpath('.//td[2]//text()').extract_first()
            state = row.xpath('.//td[3]//text()')[1].extract()
            yield {
                "rank" :rank,
                "city": city,
                "state": state
            }
