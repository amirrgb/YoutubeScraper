# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class QoutestutorialPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("myquotes.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""drop table IF EXISTS quotes_tb""")
        self.curr.execute("""create table quotes_tb(title text,author text,tag text)""")

    def process_item(self, item, spider):
        self.store_db(item)
        print("pipline :",item['title'][0])
        return item


    def store_db(self,item):                              ###this ? is for sqlite3 like %s for mysql
        try:
            self.curr.execute("""INSERT INTO quotes_tb VALUES (?,?,?)""",
                (item['title'][0],
                 item['author'][0],
                 item['tag'][0]))
        except:
            self.curr.execute("""INSERT INTO quotes_tb VALUES (?,?,?)""",
                              (item['title'][0], item['author'][0], "nothing"))
        self.conn.commit()