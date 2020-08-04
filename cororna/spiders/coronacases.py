# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class CoronacasesSpider(scrapy.Spider):
    name = 'coronacases'
    allowed_domains = ['www.worldometers.info']
    script ='''
    function main(splash, args)
        assert(splash:go(args.url))
        assert(splash:wait(6))
        tab =assert(splash:select_all('div.content-inner div a'))
        tab[3]:mouse_click()
        assert(splash:wait(3))

        return {
            html= splash:html()
        }
    end
    '''
    def start_requests(self):
        yield SplashRequest(url="https://www.worldometers.info/coronavirus/",callback=self.parse,endpoint="execute" , args={
            'lua_source' : self.script
        })


    def parse(self, response):
        for country in response.xpath('//table[@id="main_table_countries_today"]/tbody[1]/tr[position() < 225 ]'):
            yield {
                'CountryName' : country.xpath(".//td[2]/a/text()").get(),
                'Total Casses' : country.xpath(".//td[3]/text()").get(),
                'New Casses' : country.xpath(".//td[4]/text()").get(),
                'Total Deaths' : country.xpath(".//td[5]/text()").get(),
                'Total Recoverd' : country.xpath(".//td[7]/text()").get()

            }

