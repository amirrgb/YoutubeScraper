import scrapy
from jumbo_scraper.items import ProductItem


class JumboSpider(scrapy.Spider):
    name = 'jumbo'
    allowed_domains = ['jumbo.com']
    start_urls = ['https://www.jumbo.com/producten/?pageSize=24&offSet=0/']
    offset = 0

    def parse(self, response, **kwargs):
        all_products = response.css('div.card-product')

        if len(all_products) == 0:
            return

        for product in all_products:
            item = ProductItem()

            item['id'] = product.css('div::attr(data-product-id)').get().strip()

            item['link'] = 'https://www.jumbo.com/' + product.css('.title-link::attr(href)').get().strip()

            image_link = product.css('.image-container .link div img::attr(src)').get()
            item['image_link'] = None if image_link is None else image_link.strip()

            item['name'] = product.css('.title-link::text').get().strip()

            item['measure'] = ', '.join(
                [x.strip() for x in product.css('.name .subtitle p::text').extract() if x.strip() != ''])

            item['price'] = product.css('.whole::text').get().strip() + ',' + product.css(
                '.fractional::text').get().strip()

            old_price = product.css('.promo-price::text').get()

            item['old_price'] = None if old_price is None else old_price.strip()

            item['sale'] = ', '.join([x.strip() for x in product.css('.jum-tag ::text').extract() if x.strip() != ''])

            yield item

        self.offset += 24
        next_page = f'https://www.jumbo.com/producten/?pageSize=24&offSet={self.offset}/'
        yield response.follow(next_page, callback=self.parse)
