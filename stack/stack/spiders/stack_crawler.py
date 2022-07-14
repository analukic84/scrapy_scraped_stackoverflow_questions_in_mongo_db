import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import StackItem
from urllib.parse import urljoin


class StackCrawlerSpider(CrawlSpider):
    name = 'stack_crawler'
    allowed_domains = ['stackoverflow.com']

    user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Mobile Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url="https://stackoverflow.com/questions?pagesize=50&sort=newest",
                             headers={
                                 'User-Agent': self.user_agent
                             })

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[contains(@class,"s-pagination")]/a[@rel="next"]'), callback='parse_item', follow=True, process_request="set_user_agent"),
    )

    def set_user_agent(self, request, spider):
        request.headers["User-Agent"] = self.user_agent
        return request

    def parse_item(self, response):
        questions = response.xpath('//div[@id="questions"]/div')

        item = StackItem()

        for question in questions:
            item["title"] = question.xpath('normalize-space(.//div[2]/h3/a/text())').get()
            item["url"] = urljoin(base="https://stackoverflow.com/", url=question.xpath('.//div[2]/h3/a/@href').get())

            yield item
