# -*- coding: utf-8 -*-
import scrapy


class CrollSpider(scrapy.Spider):
    name = "Crunchyroll"
    allowed_domains = ["crunchyroll.com"]
    start_urls = (
        'http://www.crunchyroll.com/videos/anime/alpha?group=all',
    )

    def parse(self, response):
        self.log('A response arrived from: %s'%response.url)
