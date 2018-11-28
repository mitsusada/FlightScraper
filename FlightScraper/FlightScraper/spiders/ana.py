# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from ..items import FlightscraperItem
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class AnaSpider(scrapy.Spider):
    name = 'ana'
    allowed_domains = ['cargo.ana.co.jp']
    start_url = 'https://cargo.ana.co.jp/anaicoportal/portal/loginFlow/'
    custom_settings = {'ITEM_PIPELINES': {
                           'FlightScraper.pipelines.AnaConversionPipeline': 200,
                           }
                       }

    def start_requests(self):
        yield SeleniumRequest(
                url=self.start_url,
                callback=self.parse_result,
        )

    def wait(self, driver, element, max_time=20):
        return_element = None
        try:
            return_element = WebDriverWait(driver, max_time).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, element))
                    )
        except Exception:
            print(element + " can't get!")
            pass
        return return_element

    def parse_result(self, response):
        driver = response.meta['driver']
#        input_num = driver.find_element_by_css_selector("#trk_awbno0")

        input_num = self.wait(driver, "#trk_awbno0")
        input_num.send_keys(self.ID)
        trk_button = self.wait(driver, "#trk_btn")
        trk_button.click()
        self.wait(driver, ".padding-4 span")
        at_times = driver.find_elements_by_css_selector(".padding-4 span")
        atd = at_times[1].text
        ata = at_times[2].text

        dep_arr = driver.find_elements_by_css_selector(".blue-head-h3")
        dep = dep_arr[0].text
        arr = dep_arr[1].text

        rows = driver.find_elements_by_css_selector('.margin-bottom-30+ '
                                                    '.col-md-12 .margin-0 '
                                                    '.col-md-12')

        departure = rows[0]
        dep_comps = departure.find_elements_by_tag_name('div')

        arrived = rows[-1]
        arr_comps = arrived.find_elements_by_tag_name('div')

        flight = dep_comps[0].text
        pieces = dep_comps[-1].text.split('|')[0]
        weight = dep_comps[-1].text.split('|')[-1]

        std = dep_comps[2].find_element_by_css_selector('.margin-left-5')\
            .text.split('  ')[0].strip().rstrip(r'(STD)')
        sta = arr_comps[2].find_element_by_css_selector('.margin-left-5')\
            .text.split('  ')[-1].strip().rstrip(r'(STA)')

        date = std.split(' ')[0]

        item = FlightscraperItem()
        item['cargo_number'] = int('205' + self.ID)
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
