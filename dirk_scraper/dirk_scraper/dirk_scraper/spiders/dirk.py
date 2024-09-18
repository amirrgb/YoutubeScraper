import scrapy
from dirk_scraper.items import DirkScraperItem

MAIN_URL = 'https://www.dirk.nl'

class DirkSpider(scrapy.Spider):
    name = 'dirk'
    allowed_domains = ['dirk.nl']
    start_urls = ['https://www.dirk.nl/boodschappen']

    def parse(self, response):
        categories_link = [MAIN_URL + x for x in response.css('.product-category-header__nav a::attr(href)').getall()]
        for link in categories_link:
            yield scrapy.Request(link, callback=self.parse_categories_level1)


    def parse_categories_level1(self, response):
        categories_link = [MAIN_URL + x for x in response.css('.product-category-header__nav a::attr(href)').getall()]
        for link in categories_link:
            yield scrapy.Request(link, callback=self.parse_categories_level2)
    
    def parse_categories_level2(self, response):
        products_link = [MAIN_URL + x for x in response.css('a.product-card__image::attr(href)').getall()]
        for link in products_link:
            yield scrapy.Request(link, callback=self.parse_product)

    def parse_product(self, response):
        item = DirkScraperItem()
        name = response.css('.product-details__info__title::text').get("").strip()
        price = (response.css('.product-card__price__euros::text').get() + "." +response.css('.product-card__price__cents::text').get("0")).replace("..",".").replace(",", "")
        old_price = response.css('.product-card__price__old::text').get("").strip()
        image = response.css(".product-details__image > img::attr(src)").get()
        link = response.url
        measure = response.css('.product-details__info__subtitle::text').get("").strip()
        sale = response.css('.product-card__discount *::text').get("").strip()

        item["name"] = name
        item["price"]= price
        item["old_price"]= old_price
        item["image"]= image
        item["link"]= link
        item["measure"]= measure
        item["sale"]= sale

        yield item