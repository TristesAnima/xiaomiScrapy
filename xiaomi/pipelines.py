# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import requests
# useful for handling different item types with a single interface
from scrapy.exporters import JsonItemExporter


class XiaomiPipeline:
    def __init__(self):
        self.file = open('output.json', 'wb')
        self.exporter = JsonItemExporter(self.file, ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


def save_image(url, name):
    file_name = f"{name}.jpg"
    res = requests.get(url)
    if 200 == res.status_code:
        with open(fr"D:\pythonProject\Scrapy\xiaomiScrapy\img\{file_name}", "wb") as file:
            file.write(res.content)


class ImagePipeline:
    def __init__(self):
        self.n = 0

    def process_item(self, item, spider):
        if item["src"] != '':
            print(item["src"])
            self.n += 1
            save_image(item["src"], self.n)
        return item
