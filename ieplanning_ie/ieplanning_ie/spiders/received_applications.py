# -*- coding: utf-8 -*-
import scrapy


class ReceivedApplicationsSpider(scrapy.Spider):
    name = 'received_applications'
    allowed_domains = ['eplanning.ie']
    start_urls = ['http://eplanning.ie/']

    def parse(self, response):
        for url in response.xpath('//a/@href').extract():
            if url != '#':
                yield scrapy.Request(response.urljoin(url), callback=self.parse_application)
            else:
                self.logger.info("no such link exists")

    def parse_application(self, response):
        # self.logger.info("Parsing application")
        absolute_url = response.urljoin(response.xpath('//*[@class="glyphicon glyphicon-inbox btn-lg"]/following-sibling::a/@href').extract_first())
        yield scrapy.Request(absolute_url, callback=self.post_request)

    def post_request(self, response):
        yield scrapy.FormRequest.from_response(response, dont_filter=True, formxpath='(//form)[2]', formdata={"RdoTimeLimit": '42'}, callback=self.parse_pages)

    def parse_pages(self, response):
        for row in response.xpath('//tr')[1:]:
            relative_page_url = row.xpath('.//a/@href').extract_first()
            abs_page_url = response.urljoin(relative_page_url)
            yield scrapy.Request(abs_page_url, callback=self.parse_page)

        absolute_next_page = response.urljoin(response.xpath('//a[@rel="next"]/@href').extract_first())
        yield scrapy.Request(absolute_next_page)

    def parse_page(self, response):
        agent_btn = response.xpath('//*[@value="Agents"]/@style').extract_first()
        if 'display: inline;  visibility: visible;' in agent_btn:
            table = response.xpath('//div[@id="DivAgents"]/table')
            name = table.xpath('.//tr/td/text()')[0].extract().strip()
            address = " ".join(table.xpath('.//tr/td/text()')[1:4].extract())
            phone = table.xpath('.//tr/td/text()')[5].extract()
            email = table.xpath('.//tr/td//text()')[7].extract()

            yield {
                'name': name,
                'address': address,
                'phone': phone,
                'email': email
            }
        else:
            self.logger.info("Agents data not present")