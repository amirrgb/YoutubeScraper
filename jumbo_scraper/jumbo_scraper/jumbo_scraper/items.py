# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    id = scrapy.Field()
    link = scrapy.Field()
    image_link = scrapy.Field()
    name = scrapy.Field()
    measure = scrapy.Field()
    price = scrapy.Field()
    old_price = scrapy.Field()
    sale = scrapy.Field()
