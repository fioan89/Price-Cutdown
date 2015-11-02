__author__ = 'fauri'

import psycopg2
import settings


class PriceMonitor():
    def __init__(self, database_name='', database_user='postgres', database_password=None, host='', port=5432):
        self.database_name = database_name
        self.database_user = database_user
        self.database_password = database_password
        self.host = host
        self.port = port

    def __enter__(self):
        self.connection = psycopg2.connect(database=self.database_name, user=self.database_user,
                                           password=self.database_password, host=self.host, port=self.port)
        self.cursor = self.connection.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.connection.close()

    def monitor(self):
        pass


if __name__ == "__main__":
    with PriceMonitor() as price_monitor:
        price_monitor.monitor()