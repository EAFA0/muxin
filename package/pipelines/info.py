from scrapy import Spider


class BaseInfoPipeline:

    def process_item(self, item, spider: Spider) -> list:
        if isinstance(item, list):
            return [self.item_to_info(obj) for obj in item]
        elif isinstance(item, dict):
            return [self.item_to_info(item)]
        else:
            raise TypeError("item should be list or dict")

    def item_to_info(self, item: dict) -> dict:
        pass

    def info_from_spider(self, spider: Spider) -> dict:
        return dict(crawler=Spider.name)


class VideoInfoPipeline(BaseInfoPipeline):

    def item_to_info(self, item):
        return super().item_to_info(item)

class ImageInfoPipeline(BaseInfoPipeline):

    def item_to_info(self, item):
        return super().item_to_info(item)
