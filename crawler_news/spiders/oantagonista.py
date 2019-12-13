# -*- coding: utf-8 -*-
import scrapy
import dateutil.parser
import json

from crawler_news.items import CrawlerNewsItem, CrawlerNewsCommentItem
from crawler_news.helper import getUrls, status_urls


class OantagonistaSpider(scrapy.Spider):
    name = 'oantagonista'
    allowed_domains = ['oantagonista.com']
    start_urls = getUrls(name)

    def parse(self, response):
        # save the current page
        status_urls(self.name, response.request.url)
        # get articles
        articles = response.css("a.article_link::attr(href)")
        # crawler each article
        for article in articles:
            yield response.follow(article.extract(), self.parse_article)
        # get more articles
        next_page = response.css('link[rel=next]::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
	
    def parse_article(self, response):
        # get title
        title = response.css('h1::text').extract_first()
        # get article's date
        dt_article = response.css('time.entry-date.published::attr(datetime)').extract_first()
        # transform article's date from isodate to timestamp 
        dt_article = dateutil.parser.parse(dt_article).strftime('%s')
        # get article's section
        section = response.css('span.categoria a::text').extract_first()
        # get text
        text_article = ""
        for paragraph in response.xpath("//div[@class='entry-content']/p//text()").extract():
            text_article = text_article + paragraph

        article = CrawlerNewsItem(_id=response.request.url, title=title, date=dt_article, text=text_article, section=section)
        
        yield article
        
        # get comments
        for (text_comment, dt_comment, author_comment) in zip(response.xpath("//div[@class='comment-content']/p//text()"),
            response.css('div.comment-metadata time::attr(datetime)'), response.css('div.comment-author.vcard b::text')):
            comment = CrawlerNewsCommentItem(
              date=dateutil.parser.parse(dt_comment.extract()).strftime('%s'), # transform comments' date from isodate to timestamp
              author=author_comment.extract(),
              text=text_comment.extract(), 
              id_article=response.request.url)

            yield comment