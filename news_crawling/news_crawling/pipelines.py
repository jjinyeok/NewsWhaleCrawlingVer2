# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from news_crawling.secret import host
from news_crawling.secret import user
from news_crawling.secret import password
from news_crawling.secret import db_name
from news_crawling.secret import charset
from news_crawling.secret import port

import pymysql
class NewsCrawlingPipeline:
    
    # 스파이더 시작시 실행 - value 초기화
    def open_spider(self, spider):
        self.article_list = []

    # 크롤링 동작시 실행 
    def process_item(self, item, spider):
        self.article_list.append(item)
        return item
    
    # 스파이더 종료시 실행 - DB로 전송
    def close_spider(self, spider):
        db = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db_name,
            charset=charset,
            port=port,
        )
        cursor = db.cursor()

        # article INSERT
        article_insert_sql = '''
            INSERT IGNORE INTO article (article_title, article_reporter, article_url, article_media_name, article_media_url, article_media_image_src, article_last_modified_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        article_insert_val = []
        for article in self.article_list:
            article_insert_val.append((article['article_title'],
                article['article_reporter'],
                article['article_url'],
                article['article_media_name'],
                article['article_media_url'],
                article['article_media_image_src'],
                article['article_last_modified_date']
            ))
        cursor.executemany(article_insert_sql, article_insert_val)
       
        # keyword INSERT
        keyword_insert_sql = '''
            INSERT IGNORE INTO keyword (keyword_name, politics_count, economy_count, society_count, culture_count, international_count, local_count, sports_count, it_science_count)
            VALUES (%s, 0, 0, 0, 0, 0, 0, 0, 0)
        '''
        keyword_insert_val = []
        for article in self.article_list:
            keyword_insert_val.append((article['keyword_1'])),
            keyword_insert_val.append((article['keyword_2'])),
            keyword_insert_val.append((article['keyword_3'])),
        cursor.executemany(keyword_insert_sql, keyword_insert_val)

        # article keyword insert
        article_keyword_insert_sql = '''
            INSERT INTO article_keyword (article_id, keyword_id)
            VALUES (%s, %s)
        '''
        article_keyword_insert_val = []
        for article in self.article_list:
            article_select_sql = '''
                SELECT article_id
                FROM article
                WHERE article_title=%s
            '''
            cursor.execute(article_select_sql, article['article_title'])
            article_id = cursor.fetchall()
            keyword_select_sql = '''
                SELECT keyword_id
                FROM keyword
                WHERE keyword_name=%s
            '''
            cursor.execute(keyword_select_sql, article['keyword_1'])
            keyword_id1 = cursor.fetchall()
            cursor.execute(keyword_select_sql, article['keyword_2'])
            keyword_id2 = cursor.fetchall()
            cursor.execute(keyword_select_sql, article['keyword_3'])
            keyword_id3 = cursor.fetchall()
            article_keyword_insert_val.append((article_id[0], keyword_id1[0]))
            article_keyword_insert_val.append((article_id[0], keyword_id2[0]))
            article_keyword_insert_val.append((article_id[0], keyword_id3[0]))
        cursor.executemany(article_keyword_insert_sql, article_keyword_insert_val)

        db.commit()
        db.close()
