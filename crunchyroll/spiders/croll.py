# -*- coding: utf-8 -*-
import scrapy
import re


class CrollSpider(scrapy.Spider):
    t_pattern=re.compile('title="(.*?)"')
    name = "Crunchyroll"
    allowed_domains = ["crunchyroll.com"]
    start_urls = (
        'http://www.crunchyroll.com/videos/anime/alpha?group=all',
    )

    def parse(self, response):

        self.log('A response arrived from: %s'%response.url)
        video_container=response.xpath('//div[@class="videos-column-container cf"]')
        media_groups=response.xpath('//li[@id]')
        for anime in media_groups:
            title=anime.xpath('.//a').re(self.t_pattern)
            link=anime.xpath('.//a').xpath('.//@href').extract()[0]

            if not title:#case for anime's without a title tag in the href
                title=anime.xpath('.//a').xpath('.//text()').extract()[0].strip()
            else:
                title=title[0]

            self.log('Show: %s link: %s'%(title,link))

