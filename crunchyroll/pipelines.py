# -*- coding: utf-8 -*-
import datetime
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
from scrapy import log
import psycopg2
import crunchyroll.settings as s



class test(object):

    def __init__(self):
        self.files = {}
        
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline
        
    def spider_opened(self, spider):
        print "hello"
        
    def spider_closed(self, spider):
        print "test"


    def process_item(self, item, spider):
        print item
        return item


class CrunchyrollPipeline(object):

    def __init__(self):
        self.files = {}
        self.conn=psycopg2.connect(database=s.POSTGRES_DATABASE_NAME, user=s.POSTGRES_USER, password=s.POSTGRES_PASSWORD, )
        self.cur=self.conn.cursor()
        
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('%s_products.csv' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        for item in spider.list_of_items:
            try:
                operation=self.check_database(item)
                if operation:
                    self.put_into_database(item,operation)
                    
            except psycopg2.ProgrammingError as e:
                log.msg(message=e,_level=log.ERROR)
                self.conn.rollback()                

        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        
    def check_database(self,item):
        """Checks if the item exists in the database and what needs to be done insert, update, nothing, default is insert"""
        
        operation='INSERT'
        sql="""SELECT * FROM crunchyroll_app_series WHERE title=%s and link =%s"""
        self.cur.execute(sql,(item['title'].encode('utf-8','ignore').replace("'","\""),item['link'].encode('utf-8','ignore')))
        row=self.cur.fetchone()
        
        if row:#if row exists check to see if the description or total votes has changed
            if row[2].decode('UTF-8')!=item['description'] or int(row[10])!=int(item['total_votes']):
                operation='UPDATE'
            else:
                operation=None
                
        return operation
    
    def put_into_database(self,item,operation):
        """Puts parsed item into the database"""
        created_date=datetime.datetime.now()
        updated_date=datetime.datetime.now()
        self.exporter.export_item(item)
        parms=(item['title'].encode('utf-8','ignore').replace("'","\""),
              item['description'].encode('utf-8','ignore').replace("'","\""),
              item['link'].encode('utf-8','ignore'),
              item['average_rating'].encode('utf-8','ignore'),
              item['five_star'].replace('(','').replace(')','').encode('utf-8','ignore'),
              item['four_star'].replace('(','').replace(')','').encode('utf-8','ignore'),
              item['three_star'].replace('(','').replace(')','').encode('utf-8','ignore'),
              item['two_star'].replace('(','').replace(')','').encode('utf-8','ignore'),
              item['one_star'].replace('(','').replace(')','').encode('utf-8','ignore'),
              item['total_votes'].replace('(','').replace(')','').encode('utf-8','ignore'),
              created_date,
              updated_date)
        
        parms2=(
              item['description'].encode('utf-8','ignore').replace("'","\""),
              item['average_rating'].encode('utf-8','ignore'),
              item['five_star'].replace('(','').replace(')','').encode('utf-8','ignore'),
              item['four_star'].replace('(','').replace(')','').encode('utf-8','ignore'),
              item['three_star'].replace('(','').replace(')','').encode('utf-8','ignore'),
              item['two_star'].replace('(','').replace(')','').encode('utf-8','ignore'),
              item['one_star'].replace('(','').replace(')','').encode('utf-8','ignore'),
              item['total_votes'].replace('(','').replace(')','').encode('utf-8','ignore'),
              updated_date,
              item['title'].encode('utf-8','ignore').replace("'","\""),
              item['link'].encode('utf-8','ignore'),              
              )        
        
        sql="""insert into crunchyroll_app_series (title,description,link,average_rating,five_star,four_star,three_star,two_star,one_star,total_votes,created_date,updated_date) 
                VALUES ('%s','%s','%s',%s,%s,%s,%s,%s,%s,%s,'%s','%s');"""%parms
        
        sql_update="""UPDATE crunchyroll_app_series SET
        description='%s',
        average_rating='%s',
        five_star='%s',
        four_star='%s',
        three_star='%s',
        two_star='%s',
        one_star='%s',
        total_votes='%s',
        updated_date='%s'
        WHERE title='%s' and link='%s'
        """%parms2
        
        if operation=='UPDATE':
            sql=sql_update
        
        self.cur.execute(sql)
        self.conn.commit()

        
    def process_item(self, item, spider):
        
        return item

