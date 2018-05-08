# -*- coding: utf-8 -*-
import scrapy
import json

class Tweets2018Spider(scrapy.Spider):
    name = 'tweets2018'
    allowed_domains = ['http://trumptwitterarchive.com']
    start_urls = ['http://www.trumptwitterarchive.com/data/realdonaldtrump/2018.json']

    def parse(self, response:scrapy.http.Response):
        responseBody = response.body
        jsonResponse = json.loads(responseBody)
        for tweet in jsonResponse:
            yield {
                'created_at':  tweet['created_at'],
                'favorite_count': tweet['favorite_count'],
                'id_str': tweet['id_str'],
                'in_reply_to_user_id_str': tweet['in_reply_to_user_id_str'],
                'is_retweet': tweet['is_retweet'],
                'retweet_count': tweet['retweet_count'],
                'source': tweet['source'],
                'text': tweet['text']
            }
