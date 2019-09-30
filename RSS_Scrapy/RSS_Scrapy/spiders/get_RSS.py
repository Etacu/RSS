import scrapy
from RSS_Scrapy.items import RssReader
import psycopg2


def get_info(item, rss, id):
    if rss['id'] + item.xpath('guid/text()').extract_first().split('=')[-1] in id:
        print(item.xpath('title/text()').extract_first())
        return True
    rss['link'] = item.xpath('link/text()').extract_first()
    rss['title'] = item.xpath('title/text()').extract_first()
    categories = item.xpath('category/text()').extract()
    rss['category'] = []
    rss['id'] += item.xpath('guid/text()').extract_first().split('=')[-1]
    for category in categories:
        rss['category'].append(category)
    print(rss['link'])


def process_text(article, item):
    item['text'] = []
    item['images'] = []
    for data in article:
        text = data.xpath('text()').extract()
        if text:
            text = data.xpath('.//text()').extract()
            te = ''.join(text)
            text[0] = te
            item['text'].append(text[0])

        # 找圖片第二種
        if data.xpath('@src'):
            img = data.xpath('@src').extract_first()
            if img[0:4] == 'http':
                item['text'].append('img')
                item['images'].append(img)


def map_month(mon):
    return {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }.get(mon, 'Non')


class RSSpider(scrapy.Spider):
    name = 'RSS'

    def start_requests(self):
        conn = psycopg2.connect(database="d7jtuha77ma0q1",
                                user="eklmwiezzzuyfz",
                                password="12e338a1e992399d0b57bfce5691f20aafa834a9f439291701761a6d2289007c",
                                host="ec2-184-73-232-93.compute-1.amazonaws.com",
                                port="5432")
        cursor = conn.cursor()
        cursor.execute("select id from data1")
        spiders_id = cursor.fetchall()
        conn.close()

        id = []
        for i in spiders_id:
            id.append(i[0])

        yield scrapy.Request('http://feeds.feedburner.com/yuminghui', self.parse_yuminghui, meta={'id': id})
        yield scrapy.Request('http://feeds.feedburner.com/CommaTravel', self.parse_Commatravel, meta={'id': id})
        yield scrapy.Request('https://www.weekendhk.com/feed/', self.parse_weekendhk, meta={'id': id})
        yield scrapy.Request('https://itravelblog.net/feed/', self.parse_itravelblog, meta={'id': id})
        yield scrapy.Request('https://viablog.okmall.tw/blog/rss.php', self.parse_viablog, meta={'id': id})

    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DOWNLOAD_DELAY': 2,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'ITEM_PIPELINES': {
            'RSS_Scrapy.pipelines.PostgresqlPipeline': 300
        }
    }

    def parse(self, response):
        items = response.xpath('//item')
        for item in items:
            rss = RssReader()
            get_info(item, rss)
            yield rss

    def parse_yuminghui(self, response):
        items = response.xpath('//item')
        id = response.meta['id']
        for item in items:
            rss = RssReader()

            rss['id'] = 'yu'
            if get_info(item, rss, id):
                print('already exist')
                continue
            time = item.xpath('pubDate/text()').extract_first().split(' ')
            date = [time[3], map_month(time[2]), time[1]]
            rss['time'] = '/'.join(date)

            yield scrapy.Request(
                url=rss['link'], meta={'item': rss}, callback=self.web_yuminghui
            )

    def web_yuminghui(self, response):
        item = response.meta['item']
        item['author'] = 'morries'
        article = response.xpath('//article//p | //article//img')
        process_text(article, item)

        yield item

    def parse_Commatravel(self, response):
        items = response.xpath('//item')
        id = response.meta['id']
        for item in items:
            rss = RssReader()
            rss['id'] = 'c'
            if get_info(item, rss, id):
                print('already exist')
                continue
            time = item.xpath('pubDate/text()').extract_first().split(' ')
            date = [time[3], map_month(time[2]), time[1]]
            rss['time'] = '/'.join(date)

            yield scrapy.Request(
                url=rss['link'], meta={'item': rss}, callback=self.web_Commatravel
            )

    def web_Commatravel(self, response):
        item = response.meta['item']
        article = response.xpath('//article')
        item['author'] = article.xpath('.//p[@class="post-byline"]//a/text()').extract_first()
        process_text(article.xpath('.//div[@class="entry-inner"]//p | .//div[@class="entry-inner"]//img'), item)

        yield item

    def parse_weekendhk(self, response):
        items = response.xpath('//item')
        id = response.meta['id']
        for item in items:
            rss = RssReader()
            rss['id'] = 'whk'
            if get_info(item, rss, id):
                print('already exist')
                continue
            time = item.xpath('pubDate/text()').extract_first().split(' ')
            date = [time[3], map_month(time[2]), time[1]]
            rss['time'] = '/'.join(date)

            yield scrapy.Request(
                url=rss['link'], meta={'item': rss}, callback=self.web_weekendhk
            )

    def web_weekendhk(self, response):
        item = response.meta['item']
        item['author'] = response.xpath('//a[@itemprop="author"]/text()').extract_first()
        adasia = response.xpath('//div[@class="_content_ AdAsia"]')
        article = adasia.xpath('.//p | .//img | .//figcaption | .//h2')
        process_text(article, item)

        yield item

    def parse_itravelblog(self, response):
        items = response.xpath('//item')
        id = response.meta['id']
        for item in items:
            rss = RssReader()
            rss['id'] = 'it'
            if get_info(item, rss, id):
                print('already exist')
                continue
            time = item.xpath('pubDate/text()').extract_first().split(' ')
            date = [time[3], map_month(time[2]), time[1]]
            rss['time'] = '/'.join(date)

            yield scrapy.Request(
                url=rss['link'], meta={'item': rss}, callback=self.web_itravelblog
            )

    def web_itravelblog(self, response):
        item = response.meta['item']
        article = response.xpath('//article')
        author = article.xpath('.//span[@class="entry-author"]/a/span/text()').extract_first()
        item['author'] = author
        text = article.xpath('./div[@class="entry-content"]//p |./div[@class="entry-content"]//img')
        process_text(text[0:len(text) - 2], item)

        yield item

    def parse_viablog(self, response):
        items = response.xpath('//item')
        id = response.meta['id']
        for item in items:
            rss = RssReader()
            rss['id'] = 'v'
            if get_info(item, rss, id):
                print('already exist')
                continue
            time = item.xpath('pubDate/text()').extract_first()
            date = time[0:4], time[5:7], time[8:10]
            rss['time'] = '/'.join(date)

            yield scrapy.Request(
                url=rss['link'], meta={'item': rss}, callback=self.web_viablog
            )

    def web_viablog(self, response):
        item = response.meta['item']
        author = response.xpath('//div[@class="media-body"]/h4/text()').extract_first()
        item['author'] = author
        item['text'] = []
        item['images'] = []
        article = response.xpath('//div[@id="border-none"]')[1].xpath('div')

        for data in article:
            texts = data.xpath('text() | strong/text() | img')
            text_temp = ''
            for text in texts:
                text_ex = text.extract()
                if text_ex[0:2] != '\r\n':
                    if text.xpath('@src'):
                        img = text.xpath('@src').extract_first()
                        if img[0:4] == 'http':
                            item['text'].append('img')
                            item['images'].append(img)
                    else:
                        text_temp += text_ex
                    continue
                item['text'].append(text_temp)
                text_temp = text_ex.replace('\r\n', '')
            item['text'].append(text_temp)

        yield item
