# -*- coding: utf-8 -*-
import re

import scrapy
from urllib.parse import urljoin
from scrapy.http import Request
from bs4 import BeautifulSoup


class SaleSpider(scrapy.Spider):
    name = 'sale'
    allowed_domains = ['www.apple.com']
    start_urls = ['https://www.apple.com/jp/shop/browse/home/specialdeals/mac/']

    def parse(self, response):
        urls = response.xpath('//*[@id="primary"]/div[2]/div[2]/table/tbody/tr/td[3]/a/@href').extract()
        for url in urls:
            abs_url = urljoin('https://www.apple.com', url)
            yield Request(abs_url, callback=self.check_us_keyboard)

    def check_us_keyboard(self, response):
        select_keyboard = response.xpath('//*[@id="dimensionLanguage"]')
        if len(select_keyboard) != 0:
            soup = BeautifulSoup(response.body, "lxml")
            product_name = soup.find('h1').text.strip('\n\t')
            overview = soup.findAll("div", {"class": "as-productinfosection-panel Overview-panel row"})
            spec_info = []
            for spec in overview[0].findAll("p"):
                spec_info.append(re.sub(r'[\r|\n|\t| +]', '', spec.text))
            
            yield {'url': response.url, 'product_name': product_name, 'specs': spec_info}
        
        
