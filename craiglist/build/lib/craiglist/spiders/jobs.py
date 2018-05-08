# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['newyork.craiglist.org']
    start_urls = ['http://newyork.craigslist.org/search/jjj']

    def parse(self, response):
        results = response.xpath('//p[@class="result-info"]')
        for result in results:
            relative_job_url = result.xpath('a/@href').extract_first()
            job_title = result.xpath('a/text()').extract_first()
            posted_date = result.xpath('*[@class="result-date"]/@datetime').extract_first()
            posted_location = result.xpath('//*[@class="result-hood"]/text()').extract_first()
            absolute_job_url = response.urljoin(relative_job_url)
            yield scrapy.Request(absolute_job_url, meta={'url': absolute_job_url, 'posted_date': posted_date,
                                                         'posted_location': posted_location,
                                                         'job_title': job_title}, callback=self.parse_job_description)

        relative_next_page_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        absolute_next_page_url = "https://newyork.craigslist.org" + relative_next_page_url
        yield scrapy.Request(absolute_next_page_url)

    def parse_job_description(self, response: scrapy.http.Response):
        pass
        compensation = response.xpath('//p[@class="attrgroup"]/span/child::b/text()')[0].extract()
        employment_type = response.xpath('//p[@class="attrgroup"]/span/child::b/text()')[1].extract()
        description = response.xpath('//div[starts-with(@class, "print-information")]/following-sibling::text()').extract_first()
        url = response.meta.get('url')
        job_title = response.meta.get('job_title')
        posted_location = response.meta.get('posted_location')
        posted_date = response.meta.get('posted_date')
        yield {
            'url': url,
            'job_title': job_title,
            'posted_location': posted_location,
            'posted_date': posted_date,
            'compensation': compensation,
            'employment_type': employment_type,
            'description': description
        }
