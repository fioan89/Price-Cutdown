__author__ = 'fauri'

import psycopg2

import settings
from email_postman import GmailPostMan

SELECT_PROD_IDS_DISTINCT = "SELECT DISTINCT prod_id, name, url FROM products ORDER BY prod_id"
# Result
# [(1,'product long name', 'http://www.<provider>.com/product_location_xxssd_dsad')]

SELECT_PRICES = "SELECT price, date_of_scraping FROM prices WHERE prod_id = %s ORDER BY date_of_scraping ASC"


# Result
# [(Decimal('7999.0000'), datetime.datetime(2015, 10, 28, 9, 20, 55, 946023))]
class Item():
    def __init__(self, id, name=None, url=None, initial_price=None, last_price=None):
        self.name = name
        self.url = url
        self.inital_price = initial_price
        self.price = last_price
        self.id = id

    def __str__(self):
        header = "*" * (max(len(self.url), len(self.name)) + 2)
        return "{0}\r\n* {1}\r\n* {2}\r\n* Old Price:{3}\r\n* New Price:{4}\r\n{5}".format(header, self.name, self.url,
                                                                                           self.inital_price,
                                                                                           self.price, header)


class PriceMonitor():
    def __init__(self, database_name='', database_user='postgres', database_password=None, host='', port=5432):
        self.database_name = database_name
        self.database_user = database_user
        self.database_password = database_password
        self.host = host
        self.port = port

        # product price is 20% or lower than initial price
        self.level_one_products = []
        # product price is 30% to 20% lower than initial price
        self.level_two_products = []
        # product price is 40% to 30% lower than initial price
        self.level_three_products = []
        # product price is 50% to 40% lower than initial price
        self.level_four_products = []

    def __enter__(self):
        self.connection = psycopg2.connect(database=self.database_name, user=self.database_user,
                                           password=self.database_password, host=self.host, port=self.port)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.connection.close()

    def percent_of(self, percentage, of):
        return (of * percentage / 100)

    def _send_level_one_notifications(self, postman):
        if len(self.level_one_products) > 0:
            subject = "[Level 1] Prices went down to at least 20 percent of initial value"
            body = ""
            for item in self.level_one_products:
                body += str(item) + "\r\n\r\n"
            postman.send_to(subject=subject, message_body=body, to=settings.SEND_TO_LIST)

    def _send_level_two_notifications(self, postman):
        if len(self.level_two_products) > 0:
            subject = "[Level 2] Prices went down to at least 30 percent of initial value"
            body = ""
            for item in self.level_two_products:
                body += str(item) + "\r\n\r\n"
            postman.send_to(subject=subject, message_body=body, to=settings.SEND_TO_LIST)

    def _send_level_three_notifications(self, postman):
        if len(self.level_three_products) > 0:
            subject = "[Level 3] Prices went down to at least 40 percent of initial value"
            body = ""
            for item in self.level_three_products:
                body += str(item) + "\r\n\r\n"
            postman.send_to(subject=subject, message_body=body, to=settings.SEND_TO_LIST)

    def _send_level_four_notifications(self, postman):
        if len(self.level_four_products) > 0:
            subject = "[Level 4] Prices went down to at least 50 percent of initial value"
            body = ""
            for item in self.level_four_products:
                body += str(item) + "\r\n\r\n"
            postman.send_to(subject=subject, message_body=body, to=settings.SEND_TO_LIST)

    def send_notifications(self):
        postman = GmailPostMan(settings.GMAIL_USERNAME, settings.GMAIL_PASSWORD,
                               proxy_address=settings.SMTP_HTTP_PROXY, proxy_port=settings.SMTP_HTTP_PROXY_PORT)
        self._send_level_one_notifications(postman)
        self._send_level_two_notifications(postman)
        self._send_level_three_notifications(postman)
        self._send_level_four_notifications(postman)
        postman.close_postman()

    def monitor(self):
        """
        Monitors the prices table from db and if the values reaches certain thresholds notifications are sent.
        :return:
        """
        # first get a list of unique ids to search for in the prices
        self.cursor.execute(SELECT_PROD_IDS_DISTINCT)
        product_ids = self.cursor.fetchall()
        for id, name, url in product_ids:
            # get the prices and date of scrapping
            self.cursor.execute(SELECT_PRICES, (id,))
            prices_obj = self.cursor.fetchall()
            if len(prices_obj) >= 2:
                # TODO: move this at the db level to return only two rows - the first and the last
                initial_price = prices_obj[0][0]
                last_price = prices_obj[-1][0]
                item = Item(id, name, url, initial_price, last_price)
                # price went down to be below 20% of the inital price
                if last_price <= self.percent_of(20, initial_price):
                    self.level_one_products.append(item)
                elif last_price <= self.percent_of(30, initial_price):
                    self.level_two_products.append(item)
                elif last_price <= self.percent_of(40, initial_price):
                    self.level_three_products.append(item)
                elif last_price <= self.percent_of(50, initial_price):
                    self.level_four_products.append(item)
        # send emails if necessary
        self.send_notifications()


if __name__ == "__main__":
    with PriceMonitor(settings.PG_DATABASE, settings.PG_USER, settings.PG_PASSWORD, settings.PG_HOST,
                      settings.PG_PORT) as price_monitor:
        price_monitor.monitor()
