__author__ = 'fauri'

import sys
import os
import re
from scrapy.cmdline import execute

# this script is here just to get rid of scrapy crawl command during debuging
# with this I can simply start the process via an IDE (like PyCharm) and then enable breakpoints in my code

os.environ['http_proxy'] = "web-proxy.corp.hpecorp.net:8080"

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(execute())
