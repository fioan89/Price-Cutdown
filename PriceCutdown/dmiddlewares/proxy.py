__author__ = 'fauri'

import random

PROXY_LIST = ['http://193.231.187.92:3128:3128']

class RandomProxy(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = random.choice(PROXY_LIST)