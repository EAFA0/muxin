from scrapy import Spider


class BaseInfoPipeline:

    @classmethod
    def from_settings(cls, settings):
        return cls(settings=settings)

    def process_item(self, item, spider: Spider) -> list:
        if isinstance(item, list):
            return [self.item_to_info(obj, spider) for obj in item]
        elif isinstance(item, dict):
            return self.item_to_info(item, spider)
        else:
            raise TypeError("item should be list or dict")

    def item_to_info(self, item: dict, spider) -> dict:
        raise NotImplementedError()

class ImagesInfoPipeline(BaseInfoPipeline):

    DEFAULT_IMAGES_URLS_FIELD = 'image_urls'
    DEFAULT_IMAGES_RESULT_FIELD = 'images'

    DEFAULT_LABELS_FIELD = 'tags'

    def __init__(self, settings=None):

        self.images_urls_field = settings.get(
            'IMAGES_URLS_FIELD',
            self.DEFAULT_IMAGES_URLS_FIELD
        )
        self.images_result_field = settings.get(
            'IMAGES_RESULT_FIELD',
            self.DEFAULT_IMAGES_RESULT_FIELD
        )
        self.labels_filed = settings.get(
            'DEFAULT_LABELS_FIELD',
            self.DEFAULT_LABELS_FIELD
        )


    def item_to_info(self, item, spider):
        labels: list = item[self.labels_filed]
        labels.append(spider.name)
        
        return [result.update(labels = labels) or result
                for result in item[self.images_result_field]]


class VideosInfoPipeline(BaseInfoPipeline):

    DEFAULT_VIDEOS_URLS_FIELD = 'video_urls'
    DEFAULT_VIDEOS_RESULT_FIELD = 'videos'

    DEFAULT_LABELS_FIELD = 'tags'

    def __init__(self, settings=None):

        self.videos_urls_field = settings.get(
            'VIDEOS_URLS_FIELD',
            self.DEFAULT_VIDEOS_URLS_FIELD
        )
        self.videos_result_field = settings.get(
            'VIDEOS_RESULT_FIELD',
            self.DEFAULT_VIDEOS_RESULT_FIELD
        )
        self.labels_filed = settings.get(
            'DEFAULT_LABELS_FIELD',
            self.DEFAULT_LABELS_FIELD
        )

    def item_to_info(self, item, spider):
        labels: list = item[self.labels_filed]
        labels.append(spider.name)

        return [result.update(labels = labels) or result
                for result in item[self.videos_result_field]]
