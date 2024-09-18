from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from doctor_scraper.doctor_scraper.my_setting import MY_SETTINGS
from doctor_scraper.doctor_scraper.spiders.doctor_spider import DoctorSpiderSpider
from doctor_scraper.doctor_scraper.spiders.doctors_links_spider import DoctorLinksSpiderSpider
from doctor_scraper.doctor_scraper.spiders.doctors_fields import DoctorFieldsSpider
import csv

def change_to_formal():
    with open('doctors.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)

    for row in data:
        for i in range(len(row)):
            row[i] = row[i].replace('__', ' ')

    with open('changed_file.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


def reset_csv():
    with open("doctors_field.csv", "w", encoding="utf-8") as f:
        f.write("Field\n")
    with open("doctors.csv", "w", encoding="utf-8") as f:
        f.write("Name, Email, Phone, Address\n")
    with open("doctors_links.csv", "w", encoding="utf-8") as f:
        f.write("Link,\n")

@defer.inlineCallbacks
def crawl():
    runner = CrawlerRunner(MY_SETTINGS())
    print("collecting fields...")
    yield runner.crawl(DoctorFieldsSpider)
    print("collecting links...")
    yield runner.crawl(DoctorLinksSpiderSpider)
    print("collecting doctors...")
    yield runner.crawl(DoctorSpiderSpider)
    reactor.stop()


def remove_duplicates():
    with open('changed_file.csv', 'r') as input_file, open('output_file.csv', 'w', newline='') as output_file:
        reader = csv.reader(input_file)
        writer = csv.writer(output_file)
        seen_rows = set()
        for row in reader:
            row_tuple = tuple(row)
            if row_tuple not in seen_rows:
                writer.writerow(row)
                seen_rows.add(row_tuple)

def main():
    reset_csv()
    crawl()
    reactor.run()
    remove_duplicates()
    change_to_formal()

main()
