# -*- coding: utf-8 -*-
import scrapy


class CalSpider(scrapy.Spider):
    name = 'cal'
    allowed_domains = ['cargo.china-airlines.com']
    start_url = 'http://cargo.china-airlines.com/CCNetv2/' \
                'content/manage/ShipmentTracking.aspx/'

    def start_requests(self):
        yield SeleniumRequest(
                url=self.start_url,
                callback=self.parse_result,
        )

    def parse_result(self, response):
        print(response.meta['driver'].title)

        # Input Values
        input_form = response.meta['driver'].find_element_by_css_selector(
            '#shipmentTracking\:searchPanel2\:_idJsp36')
        input_form.send_keys(self.ID)

        # Click Add to list
        add_to_list = response.meta['driver'].find_element_by_css_selector(
            '#shipmentTracking\:searchPanel2\:_idJsp40')
        add_to_list.click()

        # Get values
        item = FlightscraperItem()
        item['cargo_number'] = int('933' + self.ID)
        item['flight'] = response.meta['driver'].find_element_by_css_selector(
            '#shipmentTracking\:trckingDetails\:_idJsp65\:0\:FlightValue').text
        item['date'] = response.meta['driver'].find_element_by_css_selector(
            '#shipmentTracking\:trckingDetails\:_idJsp65\:0\:DateValue').text
        item['departure'] = response.meta['driver'].find_element_by_css_selector(
            '#shipmentTracking\:trckingDetails\:_idJsp65\:0\:DepartureValue').text
        item['arrival'] = response.meta['driver'].find_element_by_css_selector(
            '#shipmentTracking\:trckingDetails\:_idJsp65\:0\:ArrivalValue').text
        item['pieces'] = response.meta['driver'].find_element_by_css_selector(
            '#shipmentTracking\:trckingDetails\:_idJsp65\:0\:PiecesValue').text
        item['weight'] = response.meta['driver'].find_element_by_css_selector(
            '#shipmentTracking\:trckingDetails\:_idJsp65\:0\:WeightValue').text
        item['std'] = response.meta['driver'].find_element_by_css_selector(
            '#shipmentTracking\:trckingDetails\:_idJsp65\:0\:STDValue').text
        item['sta'] = response.meta['driver'].find_element_by_css_selector(
            '#shipmentTracking\:trckingDetails\:_idJsp65\:0\:STAValue').text
        item['atd'] = response.meta['driver'].find_element_by_css_selector(
            '#shipmentTracking\:trckingDetails\:_idJsp65\:0\:EtdAtdValue1').text
        item['ata'] = response.meta['driver'].find_element_by_css_selector(
            '#shipmentTracking\:trckingDetails\:_idJsp65\:0\:EtaAtaValue1').text
        return item
