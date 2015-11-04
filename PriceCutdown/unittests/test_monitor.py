__author__ = 'fauri'

import datetime
import sys
import unittest
from decimal import Decimal


class psycopg2stub():
    @staticmethod
    def connect(database=None, user=None, password=None, host=None, port=None,
                connection_factory=None, cursor_factory=None, async=False, **kwargs):
        class ConnectionStub():
            def cursor(self):
                class CursorStub():
                    def execute(self, string_commnad, values_tuple=None):
                        self.string_command = string_commnad
                        self.value_tuple = values_tuple

                    def fetchall(self):
                        if "SELECT DISTINCT prod_id, name, url" in self.string_command:
                            return [  # level one
                                (1, 'product long name1', 'http://www.<provider>.com/product_location_1'),
                                # level one
                                (2, 'product long name2', 'http://www.<provider>.com/product_location_2'),
                                # no level
                                (3, 'product long name3', 'http://www.<provider>.com/product_location_3'),
                                # level two
                                (4, 'product long name4', 'http://www.<provider>.com/product_location_4'),
                                # level three
                                (5, 'product long name5', 'http://www.<provider>.com/product_location_5'),
                                # level three
                                (6, 'product long name6', 'http://www.<provider>.com/product_location_6'),
                                # level four
                                (7, 'product long name7', 'http://www.<provider>.com/product_location_7'),
                                # level four
                                (8, 'product long name8', 'http://www.<provider>.com/product_location_8'),
                                # level two
                                (9, 'product long name9', 'http://www.<provider>.com/product_location_9'),
                                # no level
                                (10, 'product long name10', 'http://www.<provider>.com/product_location_10'),
                            ]
                        elif self.value_tuple == (1,):  # level one
                            return [(Decimal('7999.0000'), datetime.datetime(2015, 10, 28, 9, 20, 55, 946023)),
                                    (Decimal('7998.0000'), datetime.datetime(2015, 11, 3, 14, 25, 31, 946023)),
                                    (Decimal('46.0000'), datetime.datetime(2015, 11, 3, 14, 30, 31, 946023))]
                        elif self.value_tuple == (2,):  # level one
                            return [(Decimal('800.0000'), datetime.datetime(2015, 10, 28, 9, 20, 55, 946023)),
                                    (Decimal('810.0000'), datetime.datetime(2015, 11, 3, 14, 25, 31, 946023)),
                                    (Decimal('160.0000'), datetime.datetime(2015, 11, 3, 14, 30, 31, 946023))]
                        elif self.value_tuple == (3,):  # no levlel
                            return [(Decimal('7999.0000'), datetime.datetime(2015, 10, 28, 9, 20, 55, 946023)),
                                    (Decimal('7998.0000'), datetime.datetime(2015, 11, 3, 14, 25, 31, 946023)),
                                    (Decimal('7990.0000'), datetime.datetime(2015, 11, 3, 14, 30, 31, 946023))]
                        elif self.value_tuple == (4,):  # level two
                            return [(Decimal('400.0000'), datetime.datetime(2015, 10, 28, 9, 20, 55, 946023)),
                                    (Decimal('450.0000'), datetime.datetime(2015, 11, 3, 14, 25, 31, 946023)),
                                    (Decimal('120.0000'), datetime.datetime(2015, 11, 3, 14, 30, 31, 946023))]
                        elif self.value_tuple == (5,):  # level three
                            return [(Decimal('600.0000'), datetime.datetime(2015, 10, 28, 9, 20, 55, 946023)),
                                    (Decimal('10.0000'), datetime.datetime(2015, 11, 3, 14, 25, 31, 946023)),
                                    (Decimal('240.0000'), datetime.datetime(2015, 11, 3, 14, 30, 31, 946023))]
                        elif self.value_tuple == (6,):  # level three
                            return [(Decimal('600.0000'), datetime.datetime(2015, 10, 28, 9, 20, 55, 946023)),
                                    (Decimal('605.0000'), datetime.datetime(2015, 11, 3, 14, 25, 31, 946023)),
                                    (Decimal('220.0000'), datetime.datetime(2015, 11, 3, 14, 30, 31, 946023))]
                        elif self.value_tuple == (7,):  # level four
                            return [(Decimal('800.0000'), datetime.datetime(2015, 10, 28, 9, 20, 55, 946023)),
                                    (Decimal('410.0000'), datetime.datetime(2015, 11, 3, 14, 25, 31, 946023)),
                                    (Decimal('400.0000'), datetime.datetime(2015, 11, 3, 14, 30, 31, 946023))]
                        elif self.value_tuple == (8,):  # level four
                            return [(Decimal('800.0000'), datetime.datetime(2015, 10, 28, 9, 20, 55, 946023)),
                                    (Decimal('7998.0000'), datetime.datetime(2015, 11, 3, 14, 25, 31, 946023)),
                                    (Decimal('380.0000'), datetime.datetime(2015, 11, 3, 14, 30, 31, 946023))]
                        elif self.value_tuple == (9,):  # level two
                            return [(Decimal('420.0000'), datetime.datetime(2015, 10, 28, 9, 20, 55, 946023)),
                                    (Decimal('400.0000'), datetime.datetime(2015, 11, 3, 14, 25, 31, 946023)),
                                    (Decimal('105.0000'), datetime.datetime(2015, 11, 3, 14, 30, 31, 946023))]
                        elif self.value_tuple == (10,):
                            return [(Decimal('1000.0000'), datetime.datetime(2015, 10, 28, 9, 20, 55, 946023)),
                                    (Decimal('1000.0000'), datetime.datetime(2015, 11, 3, 14, 25, 31, 946023)),
                                    (Decimal('8990.0000'), datetime.datetime(2015, 11, 3, 14, 30, 31, 946023))]

                    def close(self):
                        pass

                return CursorStub()

            def close(self):
                pass

        return ConnectionStub()


class ProxySMTPStub():
    def __init__(self, host='', port=0, p_address='', p_port=0, local_hostname=None,
                 timeout=0):
        pass

    def ehlo(self):
        pass

    def starttls(self):
        pass

    def login(self, username, password):
        pass

    def sendmail(self, email_from, to, message):
        print("From:{0}\nTo:{1}\n\n{2}".format(email_from, to, message))

    def quit(self):
        pass


from PriceCutdown import email_postman

email_postman.ProxySMTP = ProxySMTPStub

sys.modules['psycopg2'] = psycopg2stub
from PriceCutdown.monitor import PriceMonitor


class TestPriceMonitor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with PriceMonitor() as pm:
            cls.price_monitor = pm
            cls.price_monitor.monitor()

    def test_level_one_len(self):
        self.assertEquals(len(self.price_monitor.level_one_products), 2)

    def test_level_two_len(self):
        self.assertEquals(len(self.price_monitor.level_two_products), 2)

    def test_level_three_len(self):
        self.assertEquals(len(self.price_monitor.level_three_products), 2)

    def test_level_four_len(self):
        self.assertEquals(len(self.price_monitor.level_four_products), 2)


if __name__ == "__main__":
    unittest.main("test_monitor")
