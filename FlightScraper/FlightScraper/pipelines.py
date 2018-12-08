# -*- coding: utf-8 -*-

import psycopg2
import scrapy
import datetime as dt


class ValidationPipeline(object):
    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        if item['cargo_number'] is False:
            raise scrapy.exceptions.DropItem('Missing value: title')
        else:
            return item


class NcaConversionPipeline(object):
    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        if spider.name not in ['nca']:
            return item
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


class AnaConversionPipeline(object):
    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        if spider.name not in ['ana']:
            return item
        year = dt.datetime.now().year
        item['date'] = dt.datetime.strptime(item['date'],
                                            "%d-%b").replace(year)
        item['std'] = dt.datetime.strptime(item['std'],
                                           "%d-%b %Y | %H:%M")
        item['sta'] = dt.datetime.strptime(item['sta'],
                                           "%d-%b %Y | %H:%M")
        item['atd'] = dt.datetime.strptime(item['atd'],
                                           "%d-%b %Y | %H:%M")
        item['ata'] = dt.datetime.strptime(item['ata'],
                                           "%d-%b %Y | %H:%M")
        item['weight'] = item['weight'].replace('Kg', '').strip()
        item['pieces'] = item['pieces'].replace('Pcs.', '').strip()
        return item


class CalConversionPipeline(object):
    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        if spider.name not in ['cal']:
            return item
        year = dt.datetime.now().year
        item['date'] = dt.datetime.strptime(item['date'],
                                            "%d%b").replace(year)
        item['std'] = dt.datetime.strptime(item['std'].replace('(ATDL)',
                                           '').replace('(ETDL)', ''),
                                           "%d%b %H:%M").replace(year)
        item['sta'] = dt.datetime.strptime(item['sta'].replace('(ATAL)',
                                           '').replace('(ETAL)', ''),
                                           "%d%b %H:%M").replace(year)
        item['atd'] = dt.datetime.strptime(item['atd'].replace('(ATDL)',
                                           '').replace('(ETDL)', ''),
                                           "%d%b %H:%M").replace(year)
        item['ata'] = dt.datetime.strptime(item['ata'].replace('(ATAL)',
                                           '').replace('(ETAL)', ''),
                                           "%d%b %H:%M").replace(year)
        item['weight'] = item['weight'].replace('KG', '').strip()
        return item


class JalConversionPipeline(object):
    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        if spider.name not in ['jal']:
            return item
        year = dt.datetime.now().year
        item['date'] = dt.datetime.strptime(item['date'],
                                            "%d%b").replace(year)
        item['std'] = dt.datetime.strptime(item['std'].replace('(ATDL)', ''),
                                           "%d%b %H:%M").replace(year)
        item['sta'] = dt.datetime.strptime(item['sta'].replace('(ATAL)', ''),
                                           "%d%b %H:%M").replace(year)
        item['atd'] = dt.datetime.strptime(item['atd'].replace('(ATDL)', ''),
                                           "%d%b %H:%M").replace(year)
        item['ata'] = dt.datetime.strptime(item['ata'].replace('(ATAL)', ''),
                                           "%d%b %H:%M").replace(year)
        item['weight'] = item['weight'].replace('KGS', '').strip()
        return item


class CpaConversionPipeline(object):
    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        if spider.name not in ['cpa']:
            return item
        year = dt.datetime.now().year
        item['date'] = dt.datetime.strptime(item['date'],
                                            "%d %b").replace(year)
        if item['std'] is not None:
            item['std'] = dt.datetime.strptime(item['std'],
                                               "%d %b %Y%H:%M")
        if item['sta'] is not None:
            item['sta'] = dt.datetime.strptime(item['sta'],
                                               "%d %b %Y%H:%M")
        if item['atd'] is not None:
            item['atd'] = dt.datetime.strptime(item['atd'],
                                               "%d %b %Y%H:%M")
        if item['ata'] is not None:
            item['ata'] = dt.datetime.strptime(item['ata'],
                                               "%d %b %Y%H:%M")
        item['weight'] = item['weight'].replace('kg', '').strip()
        return item


class PostgresPipeline(object):
    def open_spider(self, spider: scrapy.Spider):
        uri = spider.settings.get('POSTGRESQL_URI')
        self.conn = psycopg2.connect(uri)

    def close_spider(self, spider: scrapy.Spider):
        self.conn.close()

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        sql = "UPDATE cargo_info SET flight=%s, date=%s, "\
              "departure=%s, arrival=%s, pieces=%s, weight=%s, std=%s, "\
              "sta=%s, atd=%s, ata=%s WHERE cargo_number=%s"
        curs = self.conn.cursor()
        curs.execute(sql, (item['flight'],
                           item['date'],
                           item['departure'],
                           item['arrival'],
                           item['pieces'],
                           item['weight'],
                           item['std'],
                           item['sta'],
                           item['atd'],
                           item['ata'],
                           item['cargo_number'],
                           ))
        self.conn.commit()
        return item
