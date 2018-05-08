# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo


class UsCitiesPipeline(object):
    def __init__(self):
        conn = pymongo.MongoClient(settings["MONGODB_HOST"], settings["MONGODB_PORT"])
        db = conn[settings["MONGODB_DATABASE"]]
        self.collection = db[settings["MONGODB_COLLECTION"]]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
