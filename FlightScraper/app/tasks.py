from __future__ import absolute_import, unicode_literals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .celery import app
import psycopg2
from psycopg2.extras import DictCursor
from logzero import logger

URI = 'postgresql://snakeeyes%4' \
      '0cargoflowdb:devpassword01!@cargofl' \
      'owdb.postgres.database.azure.com:54' \
      '32/snakeeyes'


def get_conn(URI):
    dsn = URI
    conn = psycopg2.connect(dsn)
    return conn


def get_resultdict_set(conn, sql="select * from cargo_info"):
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute(sql)
    results = cur.fetchall()
    dict_result = []
    for row in results:
        dict_result.append(dict(row))
    return dict_result


def main():
    process = CrawlerProcess(get_project_settings())
    print("Run Process!!!!!")
    conn = get_conn(URI)
    res_dicts = get_resultdict_set(conn)
    # no_data_dicts = [res for res in res_dicts if not all(res.values())]
    # for data_dict in no_data_dicts:
    for data_dict in res_dicts:
        cargo_number = str(data_dict['cargo_number'])
        if cargo_number.startswith('933'):
            process.crawl("nca", ID=cargo_number[3:])
        elif cargo_number.startswith('205'):
            process.crawl("ana", ID=cargo_number[3:])
        elif cargo_number.startswith('297'):
            process.crawl("cal", ID=cargo_number[3:])
        elif cargo_number.startswith('131'):
            process.crawl("jal", ID=cargo_number[3:])
        elif cargo_number.startswith('160'):
            process.crawl("cpa", ID=cargo_number[3:])
        else:
            logger.info("Unexpected prefix...")
    process.start()
#    process.join()


@app.task
def scrapy_run_crawl():
    return main()
