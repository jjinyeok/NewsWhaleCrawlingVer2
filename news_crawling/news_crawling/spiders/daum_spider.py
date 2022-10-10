import scrapy
from news_crawling.items import NewsCrawlingItem
from news_crawling.spiders.extract_keywords import extract_keywords

class DaumSpider(scrapy.Spider):
    name = 'Daum'
    allow_domain = ['https://www.daum.net/']
    start_urls = ['https://news.daum.net/']

    def parse(self, response):
        links = response.xpath('/html/body/div[2]/main/section/div/div[1]/div[1]/ul/li/div/div/strong/a/@href').extract()
        for link in links:
            yield scrapy.Request(link, headers={
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            }, callback=self.parse_content)
    
    def parse_content(self, response):
        item = NewsCrawlingItem()
        
        # article_title
        try:
            article_title = response.xpath('/html/body/div[1]/main/section/div/article/div[1]/h3/text()').extract()[0].strip()
            item['article_title'] = article_title
        except:
            article_title = ''
            item['article_title'] = article_title

        # article_reporter
        try:
            item['article_reporter'] = response.xpath('/html/body/div[1]/main/section/div/article/div[1]/div[1]/span[1]/text()').extract()[0]
        except:
            item['article_reporter'] = ''
        
        # article_url
        item['article_url'] = response.url

        # article_media_name
        try:
            item['article_media_name'] = response.xpath('/html/body/div[1]/header/div/h1/a[2]/text()').extract()[0]
        except:
            item['article_media_name'] = ''

        # article_media_url
        try:
            item['article_media_url'] = response.xpath('/html/body/div[1]/header/div/h1/a[2]/@href').extract()[0]
        except:
            item['article_media_url'] = ''

        # article_media_image_src
        item['article_media_image_src'] = '' # Daum 경우 article_media_image_src를 제공하지 않음

        # article_last_modified_date
        try:
            article_last_modified_date = response.xpath('/html/body/div[1]/main/section/div/article/div[1]/div[1]/span/span/text()').extract()[-1]
            y, m, d, time = article_last_modified_date.split()
            article_last_modified_date = y + m + d + ' ' + time
        except:
            article_last_modified_date = ''
        item['article_last_modified_date'] = article_last_modified_date

        # keyword_1, keyword_2, keyword_3
        article_content = response.xpath('/html/body/div[1]/main/section/div/article/div[2]/div[2]/section/p/text()').extract()
        temp_article_content = []
        for a in article_content:
            temp_article_content.append(a.strip())
        article_content = ' '.join(temp_article_content)
        keyword_1, keyword_2, keyword_3 = extract_keywords(article_title, article_content)
        item['keyword_1'] = keyword_1
        item['keyword_2'] = keyword_2
        item['keyword_3'] = keyword_3

        yield item
