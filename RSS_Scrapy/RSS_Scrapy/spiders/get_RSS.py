import scrapy
from RSS_Scrapy.items import RssReader


def get_info(item, rss):
    rss['link'] = item.xpath('link/text()').extract_first()
    rss['title'] = item.xpath('title/text()').extract_first()
    rss['time'] = item.xpath('pubDate/text()').extract_first()
    print(rss['link'])


def search_img(article, item):
    # 似乎還有沒有圖片的問題  需要再處理
    item['text'] = []
    item['images'] = []
    for data in article:
        text = data.xpath('text()').extract()
        if text:
            text = data.xpath('.//text()').extract()
            te = ''.join(text)
            text[0] = te
            item['text'].append(text[0])

        # 找圖片第一種方法
        # if data.xpath('.//img'):
        #    imges = data.xpath('.//img')
        #    for img in imges:
        #        text = 'img'
        #        item['text'].append(text)
        #        item['imges'].append(data.xpath('.//img/@src').extract_first())

        # 找圖片第二種
        if data.xpath('@src'):
            # new
            img = data.xpath('@src').extract_first()
            if img[0:4] == 'http':
                item['text'].append('img')
                item['images'].append(img)
            # old
            # imges = data.xpath('@src').extract()
            # for img in imges:
            #    if img[0:4] == 'http':
            #        item['text'].append('img')
            #        item['imges'].append(data.xpath('@src').extract_first())


class RSSpider(scrapy.Spider):
    name = 'RSS'

    def start_requests(self):
        yield scrapy.Request('http://feeds.feedburner.com/yuminghui', self.parse_yumin)
        yield scrapy.Request('http://feeds.feedburner.com/CommaTravel', self.parse_commatravel)
        # yield scrapy.Request('https://www.weekendhk.com/feed/', self.parse)
        yield scrapy.Request('https://itravelblog.net/feed/', self.parse_itravel)
        # yield scrapy.Request('https://viablog.okmall.tw/blog/rss.php', self.parse)

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
        for item in items:
            rss = RssReader()
            get_info(item, rss)

            yield scrapy.Request(
                url=rss['link'], meta={'item': rss}, callback=self.web_yumin
            )

    def web_yumin(self, response):
        item = response.meta['item']
        item['author'] = 'morries'
        article = response.xpath('//article//p | //article//img')
        search_img(article, item)

        yield item

    def parse_commatravel(self, response):
        items = response.xpath('//item')
        for item in items:
            rss = RssReader()
            get_info(item, rss)

            yield scrapy.Request(
                url=rss['link'], meta={'item': rss}, callback=self.web_commatravel
            )

    def web_commatravel(self, response):
        item = response.meta['item']
        article = response.xpath('//article')
        item['author'] = article.xpath('.//p[@class="post-byline"]//a/text()').extract_first()
        search_img(article.xpath('.//div[@class="entry-inner"]//p | .//div[@class="entry-inner"]//img'), item)

        yield item

    def parse_weekendhk(self, response):
        items = response.xpath('//item')
        for item in items:
            rss = RssReader()
            get_info(item, rss)

            yield scrapy.Request(
                url=rss['link'], meta={'item': rss}, callback=self.web_weekendhk
            )

    def web_weekendhk(self, response):
        item = response.meta['item']
        item['author'] = response.xpath('//a[@itemprop="author"]/text()').extract_first()

    def parse_itravel(self, response):
        items = response.xpath('//item')
        for item in items:
            rss = RssReader()
            get_info(item, rss)

            yield scrapy.Request(
                url=rss['link'], meta={'item': rss}, callback=self.web_itravel
            )

    def web_itravel(self, response):
        item = response.meta['item']
        article = response.xpath('//article')
        author = article.xpath('.//span[@class="entry-author"]/a/span/text()').extract_first()
        text = article.xpath('./div[@class="entry-content"]//p |./div[@class="entry-content"]//img')
        search_img(text[0:len(text) - 2], item)

        yield item
