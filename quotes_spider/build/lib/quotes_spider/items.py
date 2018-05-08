# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class QuotesSpiderItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass
#

class QuotesTitleTagsItemSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    item_h1_tag = scrapy.Field()
    item_tags = scrapy.Field()


class QuotesTitleTagsSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class QuotesSpiderFullItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
