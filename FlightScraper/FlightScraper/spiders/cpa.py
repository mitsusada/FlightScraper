# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from ..items import FlightscraperItem
from bs4 import BeautifulSoup


class JalSpider(scrapy.Spider):
    name = 'cpa'
    allowed_domains = ['www.cathaypacificcargo.com']
    start_url = \
        'http://www.cathaypacificcargo.com/en-us/manageyourshipment/' \
        'trackyourshipment.aspx'

    def start_requests(self):
        yield SeleniumRequest(url=self.start_url,
                              callback=self.parse_result)

    def parse_result(self, response):
        driver = response.meta['driver']
        bill_input = driver.find_element_by_id(
                'dnn_ctr779_ViewTnT_ctl00_txtAWBNo1')
        bill_input.send_keys(self.ID)
        search_button = driver.find_element_by_id(
                'dnn_ctr779_ViewTnT_ctl00_btnSearch')
        search_button.click()
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, 'lxml')
        top_elements = driver.find_elements_by_css_selector(
                '.tntSumTable .tntField')
        dep = top_elements[0].text
        arr = top_elements[1].text
        pieces = top_elements[2].text
        weight = top_elements[3].text
        bs_button = driver.find_element_by_css_selector(
                '.tntTabBtnSelected span')
        bs_button.click()
        BS_rows = soup.select('#tntTab2 .tntRow')
        oldest = BS_rows[1]
        latest = BS_rows[-1]
        oldest = [i.text for i in oldest.find_all('div')]
        latest = [i.text for i in latest.find_all('div')]
        flight = oldest[2][:6]
        pieces = oldest[5]
        std_comp = oldest[3].rstrip('(Estimated Time)').split('\xa0')
        std = std_comp[0][:len(std_comp[0])//2] + std_comp[-1] \
            if 'Estimated Time' in oldest[3] else None
        sta_comp = latest[4].rstrip('(Estimated Time)').split('\xa0')
        sta = sta_comp[0][:len(sta_comp[0])//2] + sta_comp[-1] \
            if 'Estimated Time' in latest[4] else None
        atd_comp = oldest[3].rstrip('(Actual Time)').split('\xa0')
        atd = atd_comp[0][0:len(atd_comp[0])//2] + atd_comp[-1] \
            if 'Actual Time' in oldest[3] else None
        ata_comp = latest[4].rstrip('(Actual Time)').split('\xa0')
        ata = ata_comp[0][:len(ata_comp[0])//2] + ata_comp[-1] \
            if 'Actual Time' in latest[4] else None
        date = oldest[2][6:]
        item = FlightscraperItem()
        item['cargo_number'] = int('131' + self.ID)
        item['flight'] = flight
        item['departure'] = dep
        item['arrival'] = arr
        item['pieces'] = pieces
        item['weight'] = weight
        item['std'] = std
        item['sta'] = sta
        item['atd'] = atd
        item['ata'] = ata
        item['date'] = date
        return item
