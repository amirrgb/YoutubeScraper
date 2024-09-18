import scrapy
from doctor_scraper.doctor_scraper.items import DoctorScraperItem
from tqdm import tqdm


def get_links():
    with open("doctors_links.csv", "r", encoding="utf-8") as f:
        links = f.readlines()
    links = [str(link) for link in links if "specialists" in str(link)]
    for i in range(0, len(links)):
        links[i] = links[i].replace("http", "https")
    links = list(set(links[1:30]))
    return links


class DoctorSpiderSpider(scrapy.Spider):
    name = "doctor_spider"

    def __init__(self):
        self.start_urls = get_links()
        print(len(self.start_urls))

    def start_requests(self):
        with tqdm(total=len(self.start_urls)) as pb:
            for url in self.start_urls:
                pb.update(1)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=False)

    def parse(self, response):
        item = DoctorScraperItem()
        item['doctor_name'] = str(response.xpath('//span[@class="page_title"]/text()').extract_first()).strip()
        item['doctor_email'] = response.xpath('//p[@class="profile-mail"]/span[2]/text()').extract_first().strip()
        item['doctor_phone'] = response.xpath('//p[@class="profile-phone"]/span[2]/text()').extract_first().strip()
        temp_address = response.xpath('//div[@class="profShortDtls clearfix"]/text()').extract_first().strip()
        item['doctor_address'] = str(temp_address)  # .replace(",","").strip()
        yield item
