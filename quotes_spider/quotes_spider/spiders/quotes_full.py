# -*- coding: utf-8 -*-
import scrapy


class QuotesFullSpider(scrapy.Spider):
    name = 'quotes_full'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            text = quote.xpath('.//*[@itemprop="text"]/text()').extract_first()
            author = quote.xpath('.//*[@itemprop="author"]/text()').extract_first()
            tags = quote.xpath('.//a[@class="tag"]/text()').extract()

            yield {'Text': text,
                   'Author': author,
                   'Tags': tags}

        next_page_url = response.xpath('//*[@class="next"]/a/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)

        yield scrapy.Request(absolute_next_page_url)