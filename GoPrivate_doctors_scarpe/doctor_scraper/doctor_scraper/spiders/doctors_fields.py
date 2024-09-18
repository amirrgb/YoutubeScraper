import scrapy
from doctor_scraper.doctor_scraper.items import DoctorScraperItem
from tqdm import tqdm


class DoctorFieldsSpider(scrapy.Spider):
    name = "doctors_fields"

    def __init__(self):
        self.start_urls = ["https://www.privatehealth.co.uk/specialists/"]

    def start_requests(self):
        with tqdm(total=len(self.start_urls)) as pb:
            for url in self.start_urls:
                pb.update(1)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = DoctorScraperItem()
        for field in response.xpath('//div[@class="a-to-z-menu"]/ul//li'):
            item['doctor_field'] = field.xpath(".//a/@href").get()
            yield item
