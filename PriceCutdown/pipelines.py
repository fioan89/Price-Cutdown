# -*- coding: utf-8 -*-

import psycopg2


# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

CHECK_PROD_ID = '''SELECT prod_id FROM products WHERE name LIKE %s and owner like %s'''
INSERT_PRODUCT = '''INSERT INTO products (owner, name, url) VALUES (%s, %s, %s)'''
INSERT_PRICE = '''INSERT INTO prices (prod_id, price, date_of_scraping) VALUES (%s, %s, CURRENT_TIMESTAMP)'''


class PricecutdownSQLitePipeline(object):
    def __init__(self, database_name='', database_user='postgres', database_password=None, host='', port=5432):
        self.database_name = database_name
        self.database_user = database_user
        self.database_password = database_password
        self.host = host
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            database_name=crawler.settings.get('PG_DATABASE'),
            database_user=crawler.settings.get('PG_USER'),
            database_password=crawler.settings.get('PG_PASSWORD'),
            host=crawler.settings.get('PG_HOST'),
            port=crawler.settings.get('PG_PORT')
        )

    def open_spider(self, spider):
        # TODO: check if tables exist if not execute the follwoings:
        # CREATE TABLE products (prod_id   SERIAL PRIMARY KEY, owner VARCHAR(100) NOT NULL, name      VARCHAR(4000) NOT NULL, url       VARCHAR(4000) NOT NULL);
        # CREATE TABLE prices (price_id    SERIAL PRIMARY KEY, prod_id     INTEGER REFERENCES products (prod_id), price       NUMERIC(14,4), date_of_scraping  TIMESTAMP);
        self.connection = psycopg2.connect(database=self.database_name, user=self.database_user,
                                           password=self.database_password, host=self.host, port=self.port)
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        # check if item with name exists in products. if not, insert it
        self.cursor.execute(CHECK_PROD_ID, (item['product_name'], item['product_owner']))
        product_tuple = self.cursor.fetchone()
        if not product_tuple or not product_tuple[0]:
            self.cursor.execute(INSERT_PRODUCT, (item['product_owner'], item['product_name'], item['product_link']))
            self.cursor.execute(CHECK_PROD_ID, (item['product_name'], item['product_owner']))
            product_tuple = self.cursor.fetchone()

        # insert prices
        self.cursor.execute(INSERT_PRICE, (product_tuple[0], item['product_price']))
        self.connection.commit()
        return item
