# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrunchyrollReviewItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    desciption=scrapy.Field()    
    link=scrapy.Field()

    number_of_episodes=scrapy.Field()
    
    average_rating=scrapy.Field()
    total_votes=scrapy.Field()
    one_star=scrapy.Field()
    two_star=scrapy.Field()
    three_star=scrapy.Field()
    four_star=scrapy.Field()
    five_star=scrapy.Field()
    