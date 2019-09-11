import scrapy
from RSS_Scrapy.items import RssReader


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
        links = response.xpath('//item/link/text()').extract()
        items = response.xpath('//item').extract()
        
        for item in items:
            item = RssReader()
            item['link'] = item.xpath('link/text()').extract()

        for link in links:
            item = RssReader()
            item['link'] = link
            yield scrapy.Request(
                url=link, meta={'item': item}, callback=self.get_text
            )

    def get_text(self, response):
        item = response.meta['item']
        yield item
        
print('hsis')
