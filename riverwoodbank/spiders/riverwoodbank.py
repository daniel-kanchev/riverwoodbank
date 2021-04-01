import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from riverwoodbank.items import Article


class riverwoodbankSpider(scrapy.Spider):
    name = 'riverwoodbank'
    start_urls = ['https://www.riverwoodbank.com/Blog']

    def parse(self, response):
        articles = response.xpath('//td[h2][p]')
        for article in articles:
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()
            title = article.xpath('./h2/text()[last()]').get()

            content = article.xpath('.//text()').getall()
            content = [text for text in content if text.strip() and '{' not in text]
            content = "\n".join(content[1:]).strip()

            item.add_value('title', title)
            item.add_value('content', content)

            yield item.load_item()



