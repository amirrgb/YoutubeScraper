import scrapy
from doctor_scraper.doctor_scraper.items import DoctorScraperItem
from tqdm import tqdm
import re


def get_fields_links():
    with open("doctors_field.csv", "r", encoding="utf-8") as f:
        links = f.readlines()
    links = [str(link) for link in links if "specialists" in str(link)]
    return links[1:]


def check_last_page(response):
    text = response.xpath('//div[@class="option-header"]/h2/text()')
    if text:
        return True


def process_on_address(parts):
    try:
        if not parts:
            return None
        main_address = "__".join([str(part).strip() for part in parts])
        return main_address
    except Exception as e:
        print("error processing address", str(e))
        return None


def get_next_page_url(url):
    try:
        parts = url.split("/")
        page = int(parts[-1].split("=")[-1])
        parts[-1] = "?page=%s" % (page + 1)
        return "/".join(parts)
    except Exception as e:
        print(e)
        return None


class DoctorLinksSpiderSpider(scrapy.Spider):
    name = "doctors_links_spider"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = get_fields_links()
        self.counter = 0

    def start_requests(self):
        with tqdm(total=len(self.start_urls)) as pb:
            for url in self.start_urls:
                pb.update(1)
                new_url = str(url).strip() + "/?page=1"
                yield scrapy.Request(url=new_url, callback=self.parse, dont_filter=False)

    def parse(self, response):
        if response.status in [404, 500] or check_last_page(response):
            return
        next_page_url = get_next_page_url(response.url)
        for doctor in response.xpath('//div[@class="doctor-list"]/ul//li//h4'):
            link = str(doctor.xpath(".//a/@href").get()).replace("http", "https")
            if "specialists" in str(link):
                yield response.follow(link, callback=self.parse_doctor)
                yield response.follow(link + "/contact/", callback=self.parse_doctor)

        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse)

    def parse_doctor(self, response):
        item = DoctorScraperItem()
        try:
            doctor_email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', str(response.body))
            if doctor_email:doctor_email = doctor_email[0]
            else:
                doctor_email = response.xpath('//*[@class="profile-mail"]/span[2]/text()').extract_first()
                if not doctor_email:
                    doctor_email = response.xpath('//*[@class="profile-mail"]').css('span.revealTelVal.invisible').extract_first()
        except Exception as e:
            print("email doctor",e)
            doctor_email = " "

        doctor_phone = response.xpath('//*[@class="profile-phone"]/span[2]/text()').extract_first()
        self.counter += 1
        if self.counter % 200 == 0: print(self.counter, "collected until now")
        doctor_name = response.xpath('//span[@class="page_title"]/text()').extract_first()
        if not doctor_name:
            doctor_name = response.xpath('//div[@class="bronze-profile-head-txt"]/h1/text()').extract_first()

        try:
            temp_address = response.xpath('//div[@class="mb14"]/p[2]').xpath('//span/text()').extract_first()
            if not temp_address:
                temp_address = response.xpath('//p[@class="profile-address"]').extract_first()
            if not temp_address:
                temp_address = response.xpath('//*[@id="maincontentarea"]//table//tr[1]/td[2]/div/text()').extract_first()
            temp_address = str(temp_address).replace(",", "__")
            if (not (5 < len(temp_address) < 400 )) or temp_address=="{{default_text}}": temp_address = " "
        except Exception as e:
            temp_address = " "
            print("temp_address",e)

        item['doctor_name'] = str(doctor_name).strip() if doctor_name else " "
        item['doctor_email'] = str(doctor_email).strip() if doctor_email else " "
        item['doctor_phone'] = str(doctor_phone).strip() if doctor_phone else " "
        item['doctor_address'] = str(temp_address).strip() if temp_address else " "
        if (item['doctor_email'] == ' ' or item['doctor_email'] == '') and (item['doctor_phone'] == ' ' or item['doctor_phone'] == ''): return
        yield item
