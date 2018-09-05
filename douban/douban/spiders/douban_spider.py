# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        douban_item = DoubanItem()
        movie_list = response.xpath('//ol[@class="grid_view"]/li')
        for i_item in movie_list:
            douban_item['serial_num'] = i_item.xpath('.//div[@class="item"]//em/text()').extract()[0]
            douban_item['movie_name'] = i_item.xpath('.//div[@class="info"]/div[@class="hd"]/a/span[1]/text()').extract_first()
            content = i_item.xpath('.//div[@class="info"]/div[@class="bd"]/p[1]/text()').extract()
            for i_content in content:
                content_s = ''.join(i_content.split())
                douban_item['introduction'] = content_s
            douban_item['star'] = i_item.xpath('.//span[@class="rating_num"]/text()').extract_first()
            douban_item['evaluate'] = i_item.xpath('.//div[@class="star"]//span[4]/text()').extract_first()
            douban_item['description'] = i_item.xpath('.//span[@class="inq"]/text()').extract_first()
            
            yield douban_item
        
        next_link = response.xpath('//span[@class="next"]/link/@href').extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request('https://movie.douban.com/top250'+next_link, callback=self.parse)