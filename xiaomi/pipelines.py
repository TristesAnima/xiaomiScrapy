# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

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


class ImagePipeline:
    def process_item(self, item, spider):
        n = 0
        if 'src' in item:
            n += 1
            image_url = item['src']
            image_path = os.path.join('img', n)

            response = requests.get(image_url)
            if response.status_code == 200:
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                item['image_path'] = image_path
            else:
                # 处理下载失败的情况
                item['image_path'] = None

        return item
