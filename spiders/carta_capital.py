# -*- coding: utf-8 -*-
import scrapy
import time
import datetime

from crawler_news.items import CrawlerNewsItem
from crawler_news.helper import getUrls, status_urls

class CartaCapitalSpider(scrapy.Spider):

    name = 'carta_capital'
    allowed_domains = ['cartacapital.com.br']
    start_urls = getUrls(name)

    def parse(self, response):
        # save the current page
        status_urls(self.name, response.request.url)
         # get articles
        articles = response.css("h3.eltdf-pt-three-title a::attr(href)")
        # crawler each article
        for article in articles:
            yield response.follow(article.extract(), self.parse_article)
        # get more articles
        next_page = response.css('div.eltdf-btn.eltdf-bnl-load-more.eltdf-load-more.eltdf-btn-solid a::attr(href)').extract_first()
        if next_page is not None:
	        yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        # get title
        title = response.css('h1.eltdf-title-text ::text').extract_first()
        # get sub_title
        sub_title = response.css('div.wpb_wrapper h2::text').extract_first()
        # get article's date
       	date = self.format_date(response.css('div.eltdf-post-info-date.entry-date.updated a::text').extract_first())
        # get author
        author = response.css('div.eltdf-post-info-author a ::text').extract_first()
        # get text
        text = response.css('div.eltdf-post-text-inner.clearfix ::text').extract_first()
        for paragraph in response.css('div.eltdf-post-text-inner.clearfix p::text'):
            text = (text + paragraph.extract())
        # remove footer
        text = text[:-718]
        # get section
        section = response.css('div.eltdf-post-info-category a::text').extract_first()
        # get tags
        tags = []
        for tag in response.css('div.eltdf-tags a[rel="tag"]::text'):
            tags.append(tag.extract())

        article = CrawlerNewsItem(_id=response.request.url, title=title, sub_title=sub_title, date=date, author=author, text=text, section=section, tags=tags, url=response.request.url)
        check_date(article)

        yield article

    def format_date(self, date):

        def get_mes(mes_string):
            dic = {'janeiro': '01', 'fevereiro': '02', u'mar\xe7o': '03', 'abril': '04', 'maio': '05',
            'junho': '06', 'julho': '07', 'agosto': '08', 'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12'}

            return dic[mes_string]

        def format_dia(dia):
            if(len(dia)==1):
                dia = '0' + dia

            return dia

        date = date.split()
        date_string_format = format_dia(date[0]) + "/" + get_mes(date[2]) + "/" + date[4]
        timestamp = int(time.mktime(datetime.datetime.strptime(date_string_format, "%d/%m/%Y").timetuple()))

        return timestamp
