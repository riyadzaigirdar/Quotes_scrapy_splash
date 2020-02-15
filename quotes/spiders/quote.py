# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['quotes.toscrape.com']
    
    script = '''
            function main(splash, args)
                assert(splash:go(args.url))
                assert(splash:wait(1))
                btn = assert(splash:select("li.next a"))
                btn:mouse_click()
                assert(splash:wait(1))
                
                return {
                    html = splash:html(),
                }
            end

            '''
    def start_requests(self):
        yield SplashRequest(url='http://quotes.toscrape.com',callback=self.parse)        

    def parse(self, response):
        for row in response.xpath("//div[@class='quote']"):
            txt = row.xpath(".//span[@class='text']/text()").get()
            author = row.xpath(".//span/small[@class='author']/text()").get()
            tags = row.xpath(".//div[@class='tags']/a/text()").getall()

            yield{
                'txt' : txt,
                'author' : author,
                'tags' : tags
            } 
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            abs_url = f'http://quotes.toscrape.com{next_page}'
            yield SplashRequest(url=abs_url,callback=self.parse,endpoint="execute", args={'lua_source': self.script})            