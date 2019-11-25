# -*- coding: utf-8 -*-
import json

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