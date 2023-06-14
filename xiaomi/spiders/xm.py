import scrapy
from scrapy import Selector

from xiaomi.items import XiaomiItem


class XmSpider(scrapy.Spider):
    name = "xm"
    allowed_domains = ["www.mi.com"]
    start_urls = ["https://www.mi.com/shop"]

    def parse(self, response, **kwargs):
        good_list = Selector(response).css('.home-brick-box')
        for item in good_list:
            for i in item.css('li.brick-item'):
                xmItem = XiaomiItem()
                title = i.css('.title::text').extract_first() or ''
                xmItem["title"] = title.strip()
                xmItem["desc"] = i.css('.desc::text').extract_first() or ''
                src = i.css('div.figure>img::attr(data-src)').extract_first()
                xmItem["src"] = '' if src is None else f'https:{src}'
                xmItem[
                    "price"] = f"{i.css('.price>.num::text').extract_first() or ''}{i.css('.price::text').extract_first() or ''}起"
                yield xmItem
