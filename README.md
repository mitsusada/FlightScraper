# FlightScraper
Get the tracking information from

- [NCA](https://www.nca.aero/icoportal/jsp/operations/shipment/AWBTracking.jsf)
- [ANA](https://cargo.ana.co.jp/anaicoportal/portal/loginFlow)

## Usage

1. Add the following line to the `settings.py`.

      ```
      POSTGRES_URI = YOUR_POSTGRESQL_URI
      ```

2. Execute the following command for scrape the data.  

      ```
      scrapy crawl -a [ana/nca] ID=AWB_NUMBER [-o OUTPUT_FILE]
      ```


