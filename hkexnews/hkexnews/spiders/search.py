# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest

class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['http://hkexnews.hk']
    start_urls = ['http://www.hkexnews.hk/sdw/search/searchsdw.aspx']

    def parse(self, response):
        viewstategenerator = response.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value').extract_first()
        evenvalidation = response.xpath('//*[@id="__EVENTVALIDATION"]/@value').extract_first()
        viewstate = response.xpath('//*[@id="__VIEWSTATE"]/@value').extract_first()

        data = {
            '__VIEWSTATE':viewstate,
            '__VIEWSTATEGENERATOR': viewstategenerator,
            '__EVENTVALIDATION':evenvalidation,
            'today':'20180308',
            'sortBy':'',
            'selPartID':'',
            'alertMsg':'',
            'ddlShareholdingDay':'07',
            'ddlShareholdingMonth':'03',
            'ddlShareholdingYear':'2018',
            'txtStockCode':'00001',
            'txtStockName':'',
            'txtParticipantID':'',
            'txtParticipantName':'',
            'btnSearch.x':'38',
            'btnSearch.y':'10'
        }
        #Nice and tremendous work
        request = FormRequest(url='http://www.hkexnews.hk/sdw/search/searchsdw.aspx', formdata=data)
        yield request

