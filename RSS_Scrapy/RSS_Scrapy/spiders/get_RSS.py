import scrapy
from RSS_Scrapy.items import RssReader


def get_info(item, rss):
    rss['link'] = item.xpath('link/text()').extract_first()
    rss['title'] = item.xpath('title/text()').extract_first()
    rss['time'] = item.xpath('pubDate/text()').extract_first()
    print(rss['link'])


class RSSpider(scrapy.Spider):
    name = 'RSS'

    def start_requests(self):
        yield scrapy.Request('http://feeds.feedburner.com/yuminghui', self.parse_yumin)
        # yield scrapy.Request('http://feeds.feedburner.com/CommaTravel', self.parse)
        # yield scrapy.Request('https://www.weekendhk.com/feed/', self.parse)
        # yield scrapy.Request('https://itravelblog.net/feed/', self.parse)
        # yield scrapy.Request('https://viablog.okmall.tw/blog/rss.php', self.parse)

    start_urls = [
        'https://www.weekendhk.com/feed/'
    ]
    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DOWNLOAD_DELAY': 2,
        'RANDOMIZE_DOWNLOAD_DELAY': True
    }

    def parse(self, response):
        # items = response.xpath('//item')
        #
        # for item in items[0:2]:
        #     print(response)
        #     rss = RssReader()
        #     #  update in here
        #     rss['link'] = item.xpath('link/text()').extract()
        #     rss['title'] = item.xpath('title/text()').extract()
        #     rss['time'] = item.xpath('pubDate/text()').extract()
        #     print(rss['link'])
        #
        #     yield scrapy.Request(
        #         url=rss['link'], meta={'item': rss}, callback=self.get_text
        #     )
        items = response.xpath('//item')
        for item in items:
            rss = RssReader()
            get_info(item, rss)
            yield rss

    def parse_yumin(self, response):
        items = response.xpath('//item')
        for item in items[0:3]:
            rss = RssReader()
            get_info(item, rss)

            yield scrapy.Request(
                url=rss['link'], meta={'item': rss}, callback=self.web_yumin
            )

    def web_yumin(self, response):
        item = response.meta['item']
        item['author'] = 'morries'
        item['text'] = []
        item['imges'] = []
        article = response.xpath('//article/div[@class = "entry-content"]/p')
        text = []
        img = []
        for data in article:
            item['text'].append(data.xpath('text()').extract_first())
        yield item
        
        
        
    # itravel 
    article = response.xpath('//article')
    author = article.xpath('.//spqn[@class="entry-author"]/a/text()')
    
    
    



