import scrapy
import dateutil.parser
import time

from crawler_news.items import CrawlerNewsItem, CrawlerNewsCommentItem
from crawler_news.helper import getUrls, status_urls, check_date

class Brasil247Spider(scrapy.Spider):
    name = 'brasil247'
    allowed_domains = ['brasil247.com']
    start_urls = getUrls(name)

    def parse(self, response):
        # save the current page
        status_urls(self.name, response.request.url)
        # get articles
        articles = response.css("a.articleGrid__image::attr(href)")
        # crawler each article
        for article in articles:
            yield response.follow(article.extract(), self.parse_article)
        # get more articles
        next_page = response.css('li.pagination__arrows a::attr(href)').extract()

        if next_page is not None:
            yield response.follow(next_page[-1], self.parse)

    def parse_article(self, response):
        # get title
        title = response.css('h2.article__headline.marginBottom30::text').extract_first()
        # get sub_title
        sub_title = response.css('div.article__lead p::text').extract_first()
        # get article's date
        dt_article = response.css('time.articleMetadata__info::attr(datetime)').extract_first()
        # transform article's date from isodate to timestamp
        dt_article = int(dateutil.parser.parse(dt_article).timestamp())
        # get article's section
        section = response.css('h1.header__sectionName ::text').extract_first()
        # get text
        text_article = ""
        for paragraph in response.xpath("//div[@class='article__text marginTop30']/p//text()").extract():
            text_article = text_article + paragraph

        article = CrawlerNewsItem(_id=response.request.url, title=title, sub_title=sub_title, date=dt_article, text=text_article, section=section, url=response.request.url)
        check_date(article)
        #yield article

        # get comments
        for (text_comment, author_comment) in zip(response.xpath("//div[@class='post-message ']/p//text()"), response.css('span.author.publisher-anchor-color a::text')):
            comment = CrawlerNewsCommentItem(author=author_comment.extract(), text=text_comment.extract(), id_article=response.request.url)

            yield comment
