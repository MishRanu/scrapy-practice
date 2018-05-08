# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

class QuotesLoginSpider(scrapy.Spider):
    name = 'quotes_login'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/login']

    def parse(self, response):
        token = response.xpath('//*[@name="csrf_token"]/@value').extract_first()

        return FormRequest.from_response(response, formdata={'csrf_token':token,
                                                             'password': 'foo',
                                                             'username':'foo'}, callback=self.scrape_all_quotes)

    def scrape_all_quotes(self, response):
        open_in_browser(response)
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