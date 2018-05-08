# -*- coding: utf-8 -*-
import os
import csv
import glob
import scrapy
from openpyxl import Workbook
from scrapy.loader import ItemLoader
from books_crawler.items import BooksinfoCrawlerItem
import PIL

class BooksinfoSpider(scrapy.Spider):
    name = 'booksinfo'
    allowed_domains = ['books.toscrape.com']
    # start_urls = ['http://books.toscrape.com']

    def __init__(self, category):
        self.start_urls = [category]

    def product_info(self, response, fieldname):
        xpath = '//th[text()="{}"]/./following::td/text()'.format(fieldname)
        return response.xpath(xpath).extract_first()

    def parse(self, response : scrapy.http.Response):
        for relative_url in response.xpath('//h3/a/@href').extract():
            absolute_url = response.urljoin(relative_url)
            yield scrapy.Request(absolute_url, callback=self.parse_book)

        next_page_url = response.xpath('//*[@class="next"]/a/@href').extract_first()
        absolute_url = response.urljoin(next_page_url)
        yield scrapy.Request(absolute_url)

    def parse_book(self, response):
        l = ItemLoader(item=BooksinfoCrawlerItem(), response=response)

        image_urls = response.xpath('//img/@src').extract_first().replace('../..', 'http://books.toscrape.com/')
        title = response.xpath('//h1/text()').extract_first()
        price = response.xpath('//*[@class="price_color"]/text()').extract_first()
        rating = response.xpath('//p[starts-with(@class, "star-rating")]/@class').extract_first().split(" ")[1]
        product_description = response.xpath('//*[@id="product_description"]/./following::p/text()').extract_first()
        upc = self.product_info(response, "UPC")
        productype = self.product_info(response, "Product Type")
        exprice = self.product_info(response, "Price (excl. tax)")
        inprice = self.product_info(response, "Price (incl. tax)")
        tax = self.product_info(response, "Tax")
        availability = self.product_info(response, "Availability")
        num_reviews = self.product_info(response, "Number of reviews")

        l.add_value('title', title)
        l.add_value('price', price)
        l.add_value('image_urls', image_urls)
        yield l.load_item()
        # yield {
        #     'image_urls':image_urls,
        #     'title': title,
        #     'price': price,
        #     'rating': rating,
        #     'product_description': product_description,
        #     'upc': upc,
        #     'exclusive_price': exprice,
        #     'inclusive_price': inprice,
        #     'tax': tax,
        #     'availability': availability,
        #     'number of reviews': num_reviews
        # }

    def close(self, reason):
        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)
        os.rename(csv_file, 'foobar.csv')
        # wb = Workbook()
        # ws = wb.active
        # with open(csv_file, 'r') as f:
        #     for row in csv.reader(f):
        #         ws.append(row)
        #
        # wb.save(csv_file.replace('.csv', '') + '.xlsx')
