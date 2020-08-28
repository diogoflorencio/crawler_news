# -*- coding: utf-8 -*-
import scrapy
import dateutil.parser

from crawler_news.items import CrawlerNewsItem
from crawler_news.items import CrawlerNewsCommentItem
from crawler_news.helper import getUrls, status_urls


class FolhaSpider(scrapy.Spider):

	name = 'folha'
	allowed_domains = ['folha.uol.com.br']
	start_urls = getUrls(name)

	def parse(self, response):
		# save the current page
		status_urls(self.name, response.request.url)
		# get articles
		articles = response.css("div.c-headline__content a::attr(href)")
		for article in articles:
			yield response.follow(article.extract(), self.parse_article)
		# get more articles
		next_page = response.css('li.c-pagination__arrow a::attr(href)')
		if next_page is not None:
			yield response.follow(next_page[len(next_page)-1], self.parse)

	def parse_article(self, response):
		# get title
		title = response.css('h1.c-content-head__title::text').extract_first().strip()
		# get sub_title
		sub_title = response.css('h2.c-content-head__subtitle::text').extract_first().strip()
		# get article's date transform date from isodate to timestamp
		date = dateutil.parser.parse(response.css('time.c-more-options__published-date::attr(datetime)').extract_first()).strftime('%s')
		# get author
		author = response.css('strong.c-signature__author::text').extract_first().strip()
		# get text
		text = ""
		for paragraph in response.xpath("//div[@class='c-news__body']/p//text()").extract():
			text = text + paragraph.strip()
		# get section
		section = response.css('li.c-site-nav__item.c-site-nav__item--section a::text').extract_first().strip()
		# get tags
		tags = []
		for tag in response.css('a.c-topics__link ::text'):
		    tags.append(tag.extract())

		article = CrawlerNewsItem(_id=response.request.url, title=title, sub_title=sub_title, date=date, author=author, text=text, section=section, tags=tags, url=response.request.url)

		yield article

		# get comments PROBLEMA
		for (text_comment, author_comment) in zip(response.css('div.comment-body p::text'), response.css('div.u-clearfix h3::text')):
			comment = CrawlerNewsCommentItem(author=author_comment.extract(), text=text_comment.extract(), id_article=response.request.url)
			yield comment
