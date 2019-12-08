# -*- coding: utf-8 -*-
import scrapy
import dateutil.parser
import time
import datetime

from crawler_news.items import CrawlerNewsItem
from crawler_news.helper import getUrls, status_urls

class BrasilElpaisSpider(scrapy.Spider):
    name = 'brasil_elpais'
    allowed_domains = ['brasil.elpais.com']
    start_urls = getUrls(name)

    def parse(self, response):
        # save the current page
        status_urls(self.name, response.request.url)
        # get articles
        articles = response.css("figure a ::attr(href)")
        # crawler each article
        for article in articles:
            yield response.follow(article.extract(), self.parse_article)
        # get more articles
        next_page = response.css('li.paginacion-siguiente a ::attr(href)').extract()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        # get title
        title = response.css('h1.font_secondary.color_gray_ultra_dark ::text').extract_first()
        # get sub_title
        sub_title = response.css('h2.font_secondary.color_gray_dark ::text').extract_first()
        # get article's date
        date = response.css('div.place_and_time.uppercase.color_gray_medium_lighter span::text').extract()
        # get last index
        date = self.getTimestamp(date[len(date) - 1].split())
        # get author
        author = response.css('a.color_black ::text').extract_first()
        # get text
        text = ""
        for paragraph in response.css('section.article_body.color_gray_dark p::text'):
            text = (text + paragraph.extract())
        # get tags
        tags = []
        for tag in response.css('li.tags_item.capitalize.flex.align_items_center a::text'):
            tags.append(tag.extract())
        # get section
        section = response.css('a.uppercase.overflow_hidden ::text').extract_first()

        article = CrawlerNewsItem(_id=response.request.url, title=title, sub_title=sub_title, date=date, text=text, section=section, tags=tags, url=response.request.url)

        yield article

    def getTimestamp(self, date):
        def get_mes(mes_string):
            dic = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 
            'jun': '06', 'jul': '07', 'ago': '08', 'set': '09', 'oct': '10', 'nov': '11', 'dec': '12'}
            return dic[mes_string.lower()]
        # format date
        date_string_format = date[0] + '.' + get_mes(date[1]) + '.' + date[2] + date[3] + date[4]
        # convert to timestamp
        timestamp = int(time.mktime(datetime.datetime.strptime(date_string_format, "%d.%m.%Y-%H:%M").timetuple()))
        return int(timestamp)
