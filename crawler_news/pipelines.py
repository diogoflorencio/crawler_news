# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

from crawler_news.items import CrawlerNewsItem
from crawler_news.items import CrawlerNewsCommentItem
from crawler_news.items import CrawlerNewsMetaDataItem


class CrawlerNewsPipeline(object):
    client = None
    db = None

    def open_spider(self, spider):
        # init client mongo
        self.client = MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        # set database
        self.db = self.client[settings['MONGODB_DB']]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, CrawlerNewsItem):
            self.db[spider.name].insert_one(item)
        elif isinstance(item, CrawlerNewsCommentItem):
            self.db[spider.name + 'Comments'].insert_one(dict(item))
        else:
            self.db[spider.name + 'MetaData'].insert_one(item)
        return item
