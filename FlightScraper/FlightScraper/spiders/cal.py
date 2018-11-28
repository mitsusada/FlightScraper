# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from ..items import FlightscraperItem


class CalSpider(scrapy.Spider):
    name = 'cal'
    allowed_domains = ['cargo.china-airlines.com']
    start_url = 'http://cargo.china-airlines.com/CCNetv2/' \
                'content/manage/ShipmentTracking.aspx/'
    custom_settings = {'ITEM_PIPELINES': {
                           'FlightScraper.pipelines.CalConversionPipeline': 200,
                           }
                       }

    def start_requests(self):
        yield SeleniumRequest(
                url=self.start_url,
                callback=self.parse_result,
        )

    def parse_result(self, response):
        driver = response.meta['driver']

        # Input Values
        input_form = driver.find_element_by_css_selector(
            '#ContentPlaceHolder1_txtAwbNum')
        input_form.send_keys(self.ID)

        # Click Add to list
        add_to_list = driver.find_element_by_css_selector(
            '#ContentPlaceHolder1_btnSearch')
        driver.execute_script("window.scrollTo(0, 200)")
        add_to_list.click()

        fi_comps = driver.find_elements_by_css_selector(
            '#ContentPlaceHolder1_div_FI tr+ tr td')

        flight = fi_comps[1].text
        pieces = fi_comps[4].text
        weight = fi_comps[5].text

        dep = driver.find_element_by_css_selector(
                '#ContentPlaceHolder1_rpFlightEvent_lblBrd_0').text
        arr = driver.find_element_by_css_selector(
                '#ContentPlaceHolder1_rpFlightEvent_lblOff_0').text
        std = driver.find_element_by_css_selector(
                '#ContentPlaceHolder1_rpFlightEvent_lblDepTime_0').text
        sta = driver.find_element_by_css_selector(
                '#ContentPlaceHolder1_rpFlightEvent_lblArrTime_0').text
        atd = std if '(ATDL)' in std else None
        ata = sta if '(ATAL)' in sta else None
        date = std.split(' ')[0] if std else None

        # Get values
        item = FlightscraperItem()
        item['cargo_number'] = int('297' + self.ID)
        item['flight'] = flight
        item['date'] = date
        item['departure'] = dep
        item['arrival'] = arr
        item['pieces'] = pieces
        item['weight'] = weight
        item['std'] = std
        item['sta'] = sta
        item['atd'] = atd
        item['ata'] = ata
        return item
