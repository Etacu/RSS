import scrapy
from RSS_Scrapy.RSS_Scrapy.items import RssReader


class RSSSpider(scrapy.Spider):
    name = 'RSS'
    start_urls = [
        'http://feeds.feedburner.com/yuminghui',
        'http://feeds.feedburner.com/CommaTravel',
        'https://www.weekendhk.com/feed/',
        'https://itravelblog.net/feed/',
        'https://viablog.okmall.tw/blog/rss.php'
    ]
    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DOWNLOAD_DELAY': 2,
        'RANDOMIZE_DOWNLOAD_DELAY': True
    }

    def parse(self, response):






