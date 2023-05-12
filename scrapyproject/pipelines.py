# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapyproject import settings

import psycopg2
import time

class ScrapyprojectPipeline:
    def __init__(self):
        db = settings.DATABASE
        max_retries = 10
        retry_interval = 5

        while max_retries > 0:
            try:
                self.conn = psycopg2.connect(
                    database=db['database'],
                    host=db['host'],
                    user=db['user'],
                    password=db['password'],
                )
                print("Connection successful!")

                self.cur = self.conn.cursor()
                self.cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS items (
                        id SERIAL PRIMARY KEY,
                        title TEXT NOT NULL,
                        image_url TEXT NOT NULL
                    );
                    """
                )
                
                break
            except psycopg2.OperationalError as e:
                max_retries -= 1
                if max_retries == 0:
                    print("Max retries reached. Exiting.")
                    raise e
                time.sleep(retry_interval)

    def process_item(self, item, spider):
        self.cur.execute(
                "INSERT INTO items (title, image_url) VALUES (%s, %s)",
                (item["title"], item["image_url"])
            )
        
        self.conn.commit()
        
        return item
    
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()


