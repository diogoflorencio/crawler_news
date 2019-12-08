# -*- coding: utf-8 -*-
import scrapy
import re
import time
import datetime

from crawler_news.items import CrawlerNewsItem
from crawler_news.helper import getUrls, status_urls

class EstadaoSpider(scrapy.Spider):
    name = 'estadao'
    allowed_domains = ['estadao.com.br']
    start_urls = getUrls(name)

    def parse(self, response):
        # save the current page
        status_urls(self.name, response.request.url)
        # get articles
        articles = response.css("a.link-title::attr(href)")
        # crawler each article
        for article in articles:
        	yield response.follow(article.extract(), self.parse_article)
        # get more articles
        next_page = response.css('a.pagination-control.control-first ::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        # get title
        title = response.css('h1.n--noticia__title::text').extract_first()
        # get sub_title
        sub_title = response.css('h2.n--noticia__subtitle::text').extract_first()
        # get article's date
        date = response.css('div.n--noticia__state-desc p::text').extract_first()
        if date is None:
            element = response.css('div.n--noticia__state p::text')
            author = element.extract_first()
            date = element.extract()
            # get the last index
            date = date[len(date)-1]
        else:
            # get author
            author = response.css('div.n--noticia__state-title::text').extract_first()

        # transform article's date from isodate to timestamp
        date = self.format_date(date)
        # get article's section
        section = response.css('div.header-current-page.cor-e a::text').extract_first()
        # get text
        text = ""
        for paragraph in response.css('div.n--noticia__content.content p::text').extract():
            text = text + paragraph
        # get tags
        tags = []
        for tag in response.css('a.n--noticias__tags__link::text'):
            tags.append(tag.extract())

        article = CrawlerNewsItem(_id=response.request.url, author=author, title=title, sub_title=sub_title, date=date, text=text, section=section, tags=tags, url=response.request.url)

        yield article

        # get comments
        # for (text_comment, author_comment) in zip(response.css(str('span.comment_P_1.3101312_iframe-line ::text')), response.css('span.AuthorName__name___3O4jF::text')):
        #     comment = CrawlerNewsCommentItem(
        #       author=author_comment.extract(),
        #       text=text_comment.extract(), 
        #       id_article=response.request.url)

        #     yield comment

    def format_date(self,date):
        def get_mes(mes_string):
            dic = {'janeiro': '01', 'fevereiro': '02', 'março': '03', 'abril': '04', 'maio': '05',
            'junho': '06', 'julho': '07', 'agosto': '08', 'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12'}
            return dic[mes_string]
        # format date
        date_list = date.split()
        date_string_format = date_list[0] + '.' + get_mes(date_list[2]) + '.' + date_list[4] + '-' + date_list[6]
        return int(time.mktime(datetime.datetime.strptime(date_string_format, "%d.%m.%Y-%Hh%M").timetuple()))
