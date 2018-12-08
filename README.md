# FlightScraper
Get the tracking information from

- [NCA](https://www.nca.aero/icoportal/jsp/operations/shipment/AWBTracking.jsf)
- [ANA](https://cargo.ana.co.jp/anaicoportal/portal/loginFlow)
- [JAL](http://www.jal.co.jp/en/jalcargo/inter/)
- [CAL](https://cargo.china-airlines.com/CCNetv2/content/manage/ShipmentTracking.aspx)
- [CPA](http://www.cathaypacificcargo.com/en-us/manageyourshipment/trackyourshipment.aspx)

## Usage
### Execute spider per database

1. Add the following line to the `settings.py`.

      ```
      POSTGRES_URI = YOUR_POSTGRESQL_URI
      ```

2. Execute the following command for scrape the data.  

      ```
      scrapy crawl [nca/ana/jal/cal/cpa] -a ID=AWB_NUMBER [-o OUTPUT_FILE]
      ```


### Execute all spiders

1. Enter project directory.

      ```
      cd FlightScraper
      ```

2. Execute the fololowing command in python.

      ```python
      >>> from app.tasks import main
      >>> main()
      ```
