# -*- coding: utf-8 -*-

# Scrapy settings for crunchyroll project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'crunchyroll'

SPIDER_MODULES = ['crunchyroll.spiders']
NEWSPIDER_MODULE = 'crunchyroll.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crunchyroll (+http://www.yourdomain.com)'