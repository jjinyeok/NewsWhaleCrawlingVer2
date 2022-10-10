import scrapy
from news_crawling.items import NewsCrawlingItem
from news_crawling.spiders.extract_keywords import extract_keywords

class NaverSpider(scrapy.Spider):
    name = 'Naver'
    allow_domain = ['https://www.naver.com/']
    start_urls = ['https://news.naver.com/main/ranking/popularDay.naver']

    def parse(self, response):
        links = response.xpath('//*[@id="wrap"]/div[4]/div[2]/div/div/ul/li/div/a/@href').extract()
        for link in links:
            yield scrapy.Request(link, headers={
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            }, callback=self.parse_content)
    
    def parse_content(self, response):
        item = NewsCrawlingItem()

        # article_title
        try:
            article_title = response.xpath('/html/body/div/div[2]/div/div[1]/div[1]/div[1]/div[2]/h2/text()').extract()[0].strip()
            item['article_title'] = article_title
        except:
            article_title = ''
            item['article_title'] = article_title

        # article_reporter
        try:
            item['article_reporter'] = response.xpath('/html/body/div/div[2]/div/div[1]/div[1]/div[1]/div[3]/div/a/em/text()').extract()[0]
        except:
            item['article_reporter'] = ''

        # article_url
        item['article_url'] = response.url

        # article_media_name
        try:
            item['article_media_name'] = response.xpath('/html/body/div/div[2]/div/div[1]/div[1]/div[1]/div[1]/a/img/@title').extract()[0]
        except:
            item['article_media_name'] = ''
        
        # article_media_url
        try:
            item['article_media_url'] = response.xpath('/html/body/div/div[2]/div/div[1]/div[1]/div[1]/div[1]/a/@href').extract()[0]
        except:
            item['article_media_url'] = ''

        # article_media_image_src
        try:
            item['article_media_image_src'] = response.xpath('/html/body/div/div[2]/div/div[1]/div[1]/div[1]/div[1]/a/img/@src').extract()[0]
        except:
            item['article_media_image_src'] = ''

        # article_last_modified_date
        try:
            article_last_modified_date = response.xpath('/html/body/div/div[2]/div/div[1]/div[1]/div[1]/div[3]/div/div/span/text()').extract()[-1]
        except:
            article_last_modified_date = ''
        modify_date, modify_ampm, modify_time = article_last_modified_date.split()
        article_last_modified_date = modify_date
        if modify_ampm == '오전':
            if modify_time.split(':')[0] == '12':
                article_last_modified_date += ' ' + '0' + ':' + modify_time.split(':')[1]
            else:
                article_last_modified_date += ' ' + modify_time
        elif modify_ampm == '오후':
            if modify_time.split(':')[0] == '12':
                article_last_modified_date += ' ' + modify_time
            else:
                article_last_modified_date += ' ' + str(int(modify_time.split(':')[0]) + 12) + ':' + modify_time.split(':')[1]
        item['article_last_modified_date'] = article_last_modified_date

        # keyword_1, keyword_2, keyword_3
        article_content = response.xpath('/html/body/div/div[2]/div/div[1]/div[1]/div/div/div/text()').extract()
        temp_article_content = []
        for a in article_content:
            temp_article_content.append(a.strip())
        article_content = ' '.join(temp_article_content)
        keyword_1, keyword_2, keyword_3 = extract_keywords(article_title, article_content)
        item['keyword_1'] = keyword_1
        item['keyword_2'] = keyword_2
        item['keyword_3'] = keyword_3

        yield item
