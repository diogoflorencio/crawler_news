# -*- coding: utf-8 -*-
import json
import time
import datetime

from scrapy.utils.project import get_project_settings
settings = get_project_settings()

from scrapy.exceptions import CloseSpider

# get start_urls to crawler
def getUrls(jornal):
    with open('start_urls/' + jornal + '.json') as json_file:
        data = json.load(json_file)
    return list(data.values())

# save the current page
def status_urls(jornal, url):
            with open('start_urls/' + jornal + '.json') as json_file:
                data = json.load(json_file)
            for key, value in data.items():
                if key in url:
                    data[key] = url
                    with open('start_urls/' + jornal + '.json', 'w') as outfile:
                        json.dump(data, outfile)
                    break

# check if article is within specified limit date
def check_date(article):
    limit_date = int(time.mktime(datetime.datetime.strptime(settings['LIMIT_DATE'], "%d.%m.%Y").timetuple()))
    if int(article['date']) < limit_date:
        raise CloseSpider(reason='limit_date')
