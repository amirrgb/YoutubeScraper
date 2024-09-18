# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DirkScraperItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    old_price = scrapy.Field()
    image = scrapy.Field()
    link = scrapy.Field()
    measure = scrapy.Field()
    sale = scrapy.Field()

