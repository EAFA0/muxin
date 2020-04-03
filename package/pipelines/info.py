from scrapy import Spider


class BaseInfoPipeline:


    def process_item(self, items: list, spider: Spider) -> list:
        pass

    def info_from_spider(self, spider: Spider) -> dict:
        pass

    def info_from_item(self, item: dict) -> dict:
        pass

    def info_from_body(self, body) -> dict:
        pass