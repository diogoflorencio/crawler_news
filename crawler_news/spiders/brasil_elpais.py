# -*- coding: utf-8 -*-
import scrapy
import dateutil.parser
import json

from crawler_news.items import CrawlerNewsItem


class BrasilElpaisSpider(scrapy.Spider):
    name = 'brasil_elpais'
    allowed_domains = ['brasil.elpais.com']
    start_urls = []

    def __init__(self, *a, **kw):
        super(BrasilElpaisSpider, self).__init__(*a, **kw)
        with open('start_urls/brasil_elpais.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        def status_urls(url):
            with open('start_urls/brasil_elpais.json') as json_file:
                data = json.load(json_file)
            for key, value in data.items():
                if key in response.request.url:
                    data[key] = response.request.url
                    with open('start_urls/brasil_elpais.json', 'w') as outfile:  
                        json.dump(data, outfile)
                    break
        
        status_urls(response.request.url)

        for article in response.css("article"):
            link_article = article.css("figure a::attr(href)").extract_first()
            yield response.follow(link_article, self.parse_article)
        # get more articles
        next_page = response.css('li.paginacion-siguiente a::attr(href)').extract()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        # get title
        title = response.css('h1.font_secondary.color_gray_ultra_dark ::text').extract_first()
        # get sub_title
        sub_title = response.css('h2.font_secondary.color_gray_dark ::text').extract_first()
        # get article's date
        date = '' #response.css('div.place_and_time.uppercase.color_gray_medium_lighter span::text').extract_first()
        # get author
        author = response.css('a.color_black ::text').extract_first()
        # get text
        text = ""
        for paragraph in response.css('section.article_body.color_gray_dark p::text'):
            text = (text + paragraph.extract())
        # get section
        section = response.css('a.uppercase.overflow_hidden ::text').extract_first()

        news = CrawlerNewsItem(
        title=title, sub_title=sub_title, date=date,
        author=author, text=text, section=section, _id=response.request.url)

        yield news
