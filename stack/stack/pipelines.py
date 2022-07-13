# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pymongo import MongoClient
from scrapy.exceptions import DropItem
import logging


class MongoDBPipeline(object):
    collection_name = "questions"

    def open_spider(self, spider):
        self.connection = MongoClient("<YOUR MONGO DB URI>")
        self.db = self.connection["stackoverflow"]

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        valid = True
        self.collection = self.db[MongoDBPipeline.collection_name]
        # if it is empty
        for data in item:
            if not data:
                valid = False
                raise DropItem(f"Missing {data}")
        if valid:
            if self.collection.find_one({"title": item["title"]}):
                logging.info("Data exists.")
            else:
                self.collection.insert_one(dict(item))
                logging.info("Question added to MongoDB base")
        return item