## Task  was to scrap questions and urls from stackoverflow questions page, handle pagination and save into mongoDB using Scrapy

url = https://stackoverflow.com/questions?pagesize=50&sort=newest

### stack_spider.py
Because this page have a lot of pages... I force to stop scraping when access 6th page

### stack_crawler.py
using Rule to iterate over pages

In both cases
MongoDB URI need to be updated with the valid one.

While storing questions in MongoDB, program checks does exist the current question. If yes, raise DropItem exception (stop processing an Item), if not add question to MongoDB.
