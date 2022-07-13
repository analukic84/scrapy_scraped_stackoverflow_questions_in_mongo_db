import scrapy
from ..items import StackItem
from urllib.parse import urljoin
from scrapy.exceptions import CloseSpider


class ScrapySpider(scrapy.Spider):
    name = "stackspider"
    allowed_domains = ["stackoverflow.com"]

    def start_requests(self):
        yield scrapy.Request(url="https://stackoverflow.com/questions?pagesize=50&sort=newest",
                             callback=self.parse,
                             headers={
                                 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Mobile Safari/537.36'
                             })

    def parse(self, response):
        questions = response.xpath('//div[@id="questions"]/div')

        item = StackItem()

        for question in questions:
            item["title"] = question.xpath('normalize-space(.//div[2]/h3/a/text())').get()
            item["url"] = urljoin(base="https://stackoverflow.com/", url=question.xpath('.//div[2]/h3/a/@href').get())

            yield item

        next_page = urljoin(base="https://stackoverflow.com/", url=response.xpath('//div[contains(@class,"s-pagination")]/a[@rel="next"]/@href').get())
        # Go to page 2
        next_page_number = response.xpath('//div[contains(@class,"s-pagination")]/a[@rel="next"]/@title').get()

        if next_page_number == "Go to page 6":
            raise CloseSpider("We ended with the page 6")
        else:
            if next_page:
                yield scrapy.Request(url=next_page,
                                     callback=self.parse,
                                     headers={
                                         'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Mobile Safari/537.36'
                                     })

