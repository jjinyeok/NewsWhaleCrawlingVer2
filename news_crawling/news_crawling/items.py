# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsCrawlingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    article_title = scrapy.Field()
    article_reporter = scrapy.Field()
    article_url = scrapy.Field()
    article_media_name = scrapy.Field()
    article_media_url = scrapy.Field()
    article_media_image_src = scrapy.Field()
    article_last_modified_date = scrapy.Field()
    keyword_1 = scrapy.Field()
    keyword_2 = scrapy.Field()
    keyword_3 = scrapy.Field()
