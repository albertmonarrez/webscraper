# -*- coding: utf-8 -*-
import scrapy
import scrapy.http.request
import re
import crunchyroll.items as items


class CrollSpider(scrapy.Spider):
    t_pattern=re.compile('title="(.*?)"')
    name = "Crunchyroll"
    allowed_domains = ["crunchyroll.com"]
    start_urls = (
        'http://www.crunchyroll.com/videos/anime/alpha?group=all',
    )
    main_page='http://www.crunchyroll.com'
    list_of_items=[]

    def parse(self, response):

        self.log('A response arrived from: %s'%response.url)
        video_container=response.xpath('//div[@class="videos-column-container cf"]')
        media_groups=response.xpath('//li[@id]')
        
        for anime in media_groups:
            show=items.CrunchyrollReviewItem()
            title=anime.xpath('.//a').re(self.t_pattern)
            link=anime.xpath('.//a').xpath('.//@href').extract()[0]

            if not title:#case for anime's without a title tag in the href
                title=anime.xpath('.//a').xpath('.//text()').extract()[0].strip()
            else:
                title=title[0]
            
            self.log('Show: %s link: %s%s'%(title,self.main_page,link))
            
            show['title']=title
            show['link']=link
            
            request=scrapy.http.Request(self.main_page+link+'/reviews',callback=self.parse_job)
            request.meta['show']=show#pass in my show item so I can fill it up some more with the callback
            
            yield request
            
    def parse_job(self, response):
        print response.meta['show']

