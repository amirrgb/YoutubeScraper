# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoctorScraperItem(scrapy.Item):
    doctor_name = scrapy.Field()
    doctor_email = scrapy.Field()
    doctor_phone = scrapy.Field()
    doctor_address = scrapy.Field()
    doctor_link = scrapy.Field()
    doctor_field = scrapy.Field()