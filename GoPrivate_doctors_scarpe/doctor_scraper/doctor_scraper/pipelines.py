# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
def save_into_csv(item):
    try:
        with open("doctors.csv", "a", encoding="utf-8") as f:
            f.write(f"{item['doctor_name'] if item['doctor_name'] else ''}, {item['doctor_phone'] if item['doctor_phone'] else ''}, {item['doctor_email'] if item['doctor_email'] else ''}, {item['doctor_address'] if item['doctor_address'] else ''}\n")
    except:
        print("error saving")

def save_into_field_csv(item):
    try:
        with open("doctors_field.csv", "a", encoding="utf-8") as f:
            f.write(f"{item['doctor_field']}\n")
    except:
        print("error saving fields")


def save_links_csv(item):
    try:
        with open("doctors_links.csv", "a", encoding="utf-8") as f:
            f.write(f"{item['doctor_link']}\n")
    except:
        print("error saving link")

class DoctorScraperPipeline:
    def process_item(self, item, spider):
        if 'doctor_field' in item and item['doctor_field'] != "":
            save_into_field_csv(item)
        if 'doctor_name' in item and item['doctor_name'] != "":
            save_into_csv(item)
        elif 'doctor_link' in item and item['doctor_link'] != "":
            save_links_csv(item)
        return item