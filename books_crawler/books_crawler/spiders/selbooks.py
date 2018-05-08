# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException


class SelbooksSpider(scrapy.Spider):
    name = 'selbooks'
    allowed_domains = ['books.toscrape.com']

    def start_requests(self):

        self.driver = webdriver.Chrome('D:\study\python_exercise\scrapy-practice\\books_crawler\\chromedriver.exe')
        self.driver.get("http://books.toscrape.com")
        base_url = "http://books.toscrape.com/"

        sel = scrapy.selector.Selector(text=self.driver.page_source)
        # self.driver.find_element_by_xpath('//*[@class=next]/a').click()
        relative_urls = sel.xpath('//h3/a/@href').extract()

        for relative_url in relative_urls:
            absolute_url = base_url + relative_url
            yield scrapy.Request(absolute_url, callback=self.parse_book)

        while True:
            try:
                next_page = self.driver.find_element_by_xpath('//*[@class="next"]/a')
                sleep(3)
                self.logger.info("Sleeping for 3 secs")
                next_page.click()
                sel = scrapy.selector.Selector(text=self.driver.page_source)
                relative_urls = sel.xpath('//h3/a/@href').extract()
                for relative_url in relative_urls:
                    absolute_url = base_url + "catalogue/" + relative_url
                    yield scrapy.Request(absolute_url, callback= self.parse_book)
            except NoSuchElementException:
                self.logger.info("Finished scraping exit")
                self.driver.quit()
                break


    def parse_book(self, response):
        pass
