# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from ..items import FlightscraperItem
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


class JalSpider(scrapy.Spider):
    name = 'jal'
    allowed_domains = ['www.jal.co.jp']
    start_url = 'http://www.jal.co.jp/en/jalcargo/inter/'

    def start_requests(self):
        yield SeleniumRequest(url=self.start_url,
                              callback=self.parse_result)

    def parse_result(self, response):
        driver = response.meta['driver']
        bill_input = driver.find_element_by_css_selector('#S_AIR_WAYBILL_S01')
        bill_input.send_keys(self.ID)
        search_button = driver.find_element_by_css_selector('#SEARCH_SUBMIT')
        search_button.click()
        dep = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            '.clearfix div:nth-child(1) p')
                                           )
        )
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, 'lxml')
        dep = soup.select_one('.clearfix div:nth-of-type(1) p').text
        arr = soup.select_one('.clearfix div:nth-of-type(2) p').text
        pieces = soup.select_one('.clearfix div:nth-of-type(3) p').text
        weight = soup.select_one('.clearfix div:nth-of-type(4) p').text
        departed_list = soup.find_all('th', string='Departed')
        departed_comps = [i.find_next_siblings('td') for i in departed_list]
        first_departed = [i.text for i in departed_comps[0]]
        arrived_list = soup.find_all('th', string='Arrived')
        arrived_comps = [i.find_next_siblings('td') for i in arrived_list]
        last_arrived = [i.text for i in arrived_comps[-1]]
        flight = first_departed[1]
        date = first_departed[-2]
        std = ' '.join((date, first_departed[-1]))
        sta = ' '.join((date, last_arrived[-1]))
        atd = ' '.join((date, first_departed[-1]))
        ata = ' '.join((date, last_arrived[-1]))
        item = FlightscraperItem()
        item['cargo_number'] = int('131' + self.ID)
        item['flight'] = flight
        item['departure'] = dep
        item['arrival'] = arr
        item['pieces'] = pieces
        item['weight'] = weight
        item['flight'] = flight
        item['std'] = std
        item['sta'] = sta
        item['atd'] = atd
        item['ata'] = ata
        item['date'] = date
        return item
