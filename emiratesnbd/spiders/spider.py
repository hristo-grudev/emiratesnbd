import scrapy

from scrapy.loader import ItemLoader

from ..items import EmiratesnbdItem
from itemloaders.processors import TakeFirst


class EmiratesnbdSpider(scrapy.Spider):
	name = 'emiratesnbd'
	start_urls = ['https://www.emiratesnbd.com/en/media-centre/?ref=homepage-news&etm_action=hw-news&etm_content=hw-f16-news-2O8CwDnu']

	def parse(self, response):
		post_links = response.xpath('//div[contains(@class,"news-item")]')
		for post in post_links:
			url = post.xpath('.//a/@href').get()
			date = post.xpath('.//p[contains(@class,"tc-color-13 m-0")]/text()').get()
			title = post.xpath('.//h3/strong/text()').get()
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date, 'title': title})

	def parse_post(self, response, title, date):
		description = response.xpath('//div[@class="fs-l mo-fs-m pb-50"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()

		item = ItemLoader(item=EmiratesnbdItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
