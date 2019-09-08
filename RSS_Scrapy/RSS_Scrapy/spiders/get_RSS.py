import scrapy
from RSS_Scrapy.RSS_Scrapy.items import RssReader


class RSSSpider(scrapy.Spider):
    name = 'RSS'
    allowed_domains = ['']

