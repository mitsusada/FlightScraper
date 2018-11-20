# -*- coding: utf-8 -*-

import scrapy


class FlightscraperItem(scrapy.Item):
    cargo_number = scrapy.Field()
    flight = scrapy.Field()
    date = scrapy.Field()
    departure = scrapy.Field()
    arrival = scrapy.Field()
    pieces = scrapy.Field()
    weight = scrapy.Field()
    std = scrapy.Field()
    sta = scrapy.Field()
    atd = scrapy.Field()
    ata = scrapy.Field()


