# -*- coding: utf-8 -*-
import scrapy
import json
import time
import datetime

from crawler_news.items import CrawlerNewsItem
from crawler_news.items import CrawlerNewsCommentItem
from crawler_news.helper import getUrls, status_urls

class GazetaDoPovoSpider(scrapy.Spider):

	name = 'gazeta_do_povo'
	allowed_domains = ['gazetadopovo.com.br']
	start_urls = getUrls(name)

	def parse(self, response):
		# save the current page
		status_urls(self.name, response.request.url)
        # get articles
		articles = response.css("article")
        # crawler each article
		for article in articles:
			link_article = 'https://gazetadopovo.com.br' + str(article.css("a ::attr(href)").extract_first())
			yield response.follow(link_article, self.parse_article)
		# get more articles
		next_page = response.css('a[aria-label="Próxima Página"] ::attr(href)').extract_first()
		if next_page is not None:
			yield response.follow(next_page, self.parse)

	def parse_article(self, response):
		# get title
		title = response.css('h1.c-title ::text').extract_first()
		# get sub_title
		sub_title = response.css('div.c-mobile-relative h2 ::text').extract_first()
		# get author
		author = response.css('div.item-name-author span::text').extract_first()[4:]
		# get date
		date = self.format_date(response.css('div.c-credits li::text').extract_first())
		# get section
		section = response.request.url.split('/')[3]
		# get text
		text=""
		for paragraph in response.xpath("//div[@class='paywall-google']/p//text()"):
			text = (text + paragraph.extract())
		# get tags
		tags = []
		for tag in response.css('div.c-list-tags a::text'):
			tags.append(tag.extract())

		article = CrawlerNewsItem(title=title, sub_title=sub_title, author=author, date=date, text=text, section=section, tags=tags, _id=response.request.url)

		yield article

		# get comments
		for (author_comment, text_comment, like_comment, dislike_comment, dt_comment) in zip(response.css('p.user-name ::text'),
			response.css('p.comment ::text'), response.css('a.like span::text'), response.css('a.dislike span::text'), response.css('p.age ::text')):
			comment = CrawlerNewsCommentItem(
              likes=like_comment.extract(),
              dislikes=dislike_comment.extract(),
              author=author_comment.extract(),
              text=text_comment.extract(),
              date= self.format_date_comment(dt_comment.extract()[2]),
              id_article=response.request.url)

			yield comment

	def format_date(self, date):
		date_string_format = str(date)[1:11] + '-' + str(date)[14:19]
		timestamp = int(time.mktime(datetime.datetime.strptime(date_string_format, "%d/%m/%Y-%H:%M").timetuple()))

		return timestamp

	def format_date_comment(self, days):
		date_N_days_ago = datetime.datetime.now() - datetime.timedelta(days=int(days))

		return int(time.mktime(date_N_days_ago.timetuple()))
