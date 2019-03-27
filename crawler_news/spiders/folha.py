# -*- coding: utf-8 -*-
import scrapy
import dateutil.parser

from crawler_news.items import CrawlerNewsItem
from crawler_news.items import CrawlerNewsCommentItem


class FolhaSpider(scrapy.Spider):
	name = 'folha'
	allowed_domains = ['folha.uol.com.br']
	start_urls = ['http://search.folha.uol.com.br/search?q=de&periodo=personalizado&sd=01%2F01%2F2010&ed=31%2F12%2F2018&site=sitefolha&site%5B%5D=online']

	def parse(self, response):
		for article in response.css("div.c-headline__content a::attr(href)"):
			yield response.follow(article.extract(), self.parse_article)
		# get more articles
		next_page = response.css('li.c-pagination__arrow a::attr(href)')
		if next_page is not None:
			yield response.follow(next_page[len(next_page)-1], self.parse
)
	def parse_article(self, response):
		# get title
		title = response.css('h1.c-content-head__title::text').extract_first()
		# get sub_title
		sub_title = response.css('h2.c-content-head__subtitle::text').extract_first()
		# get article's date transform date from isodate to timestamp
		date = 0 #dateutil.parser.parse(response.css('time.c-more-options__published-date::attr(datetime)').extract_first()).strftime('%s') 
		# get author
		author = response.css('strong.c-signature__author::text').extract_first()
		# get text
		text = ""
		for paragraph in response.xpath("//div[@class='c-news__body']/p//text()").extract():
			text = text + paragraph
		# get section
		section = response.css('li.c-site-nav__item c-site-nav__item--section a::text').extract_first()  

		news = CrawlerNewsItem(
		_id=response.request.url,title=title, sub_title=sub_title, date=date,
		author=author, text=text, section=section, url=response.request.url)

		# yield news

		#get commmets
		for (text_comment,dt_comment, author_comment) in zip(response.css('div.comment-body p::text'),
			response.css('div.u-clearfix span::text'), response.css('div.u-clearfix h3::text')):
			# comment = CrawlerNewsCommentItem(
			# 	date=dateutil.parser.parse(dt_comment.extract()).strftime('%s'),
			# 	author=author_comment.extract(),
			# 	text=text_comment.extract(),
			# 	id_article=link_article)
			# yield comment
			print('\n\n\n')
			print(self.format_date(dt_comment.extract()))
			print('\n\n\n')
			
		
	def format_date(date):
		delimiters_date = u'[^a-zA-Z0-9]'
		date_list = re.sub(delimiters_date, ' ', date).split()
		date_string_format = date_list[0] + '.' + date_list[1] + '.' + date_list[2] + '-' + date_list[3]
		return int(time.mktime(datetime.datetime.strptime(date_string_format, "%d.%m.%Y-%Hh%M").timetuple()))
