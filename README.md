# FlightScraper
Get the tracking information from [NCA](https://www.nca.aero/icoportal/jsp/operations/shipment/AWBTracking.jsf)


## Usage

1. Add the following line to the `settings.py`.

      ```
      POSTGRES_URI = YOUR_POSTGRESQL_URI
      ```

2. Execute the following command for scrape the data from [NCA](https://www.nca.aero/icoportal/jsp/operations/shipment/AWBTracking.jsf).  

      ```
      scrapy crawl -a ID=AWB_NUMBER [-o OUTPUT_FILE]
      ```


