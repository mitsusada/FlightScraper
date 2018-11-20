# -*- coding: utf-8 -*-

import psycopg2
import scrapy
import datetime as dt


class ValidationPipeline(object):
    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        if item['cargo_number'] is False:
            raise scrapy.exceptions.DropItem('Missing value: title')
        return item


class ConversionPipeline(object):
    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        year = dt.datetime.now().year
        item['date'] = dt.datetime.strptime(item['date'],
                                            "%d%b").replace(year)
        item['std'] = dt.datetime.strptime(item['std'],
                                           "%d%b %H:%M").replace(year)
        item['sta'] = dt.datetime.strptime(item['sta'],
                                           "%d%b %H:%M").replace(year)
        item['atd'] = dt.datetime.strptime(item['atd'],
                                           "%d%b %H:%M").replace(year)
        item['ata'] = dt.datetime.strptime(item['ata'],
                                           "%d%b %H:%M").replace(year)
        return item


class PostgresPipeline(object):
    def open_spider(self, spider: scrapy.Spider):
        uri = spider.settings.get('POSTGRESQL_URI')
        self.conn = psycopg2.connect(uri)

    def close_spider(self, spider: scrapy.Spider):
        self.conn.close()

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        sql = "INSERT INTO cargo_info (cargo_number, flight, date, "\
              "departure, arrival, pieces, weight, std, sta, atd, "\
              "ata) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        curs = self.conn.cursor()
        curs.execute(sql, (item['cargo_number'],
                           item['flight'],
                           item['date'],
                           item['departure'],
                           item['arrival'],
                           item['pieces'],
                           item['weight'],
                           item['std'],
                           item['sta'],
                           item['atd'],
                           item['ata'],
                           ))
        self.conn.commit()
        return item
