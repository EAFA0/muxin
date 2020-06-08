class FilesInfoPipeline:

    DEFAULT_URLS_FIELD = 'file_urls'
    DEFAULT_RESULTS_FIELD = 'files'

    DEFAULT_LABELS_FIELD = 'tags'

    def __init__(self, settings=None):

        self.urls_field = settings.get(
            'FILES_URLS_FIELD',
            self.DEFAULT_URLS_FIELD
        )
        self.labels_filed = settings.get(
            'LABELS_FIELD',
            self.DEFAULT_LABELS_FIELD
        )
        self.results_field = settings.get(
            'FILES_RESULTS_FIELD',
            self.DEFAULT_RESULTS_FIELD
        )

    @classmethod
    def from_settings(cls, settings):
        return cls(settings=settings)

    def process_item(self, item, spider) -> list:
        if isinstance(item, list):
            return [self.item_to_info(obj, spider) for obj in item]
        elif isinstance(item, dict):
            return self.item_to_info(item, spider)
        else:
            raise TypeError("item should be list or dict")

    def item_to_info(self, item: dict, spider) -> dict:
        # url 信息和 result 中的 url 信息重复
        item.pop(self.urls_field)

        labels = item.pop(self.labels_filed)
        results = item.pop(self.results_field)

        if isinstance(results, list):
            return [self.result_to_info(result, item, labels)
                    for result in results]
        elif isinstance(results, dict):
            return [self.result_to_info(results, item, labels)]
        else:
            raise TypeError(f"The results obj should be list / dict, get {type(results)}")

    def result_to_info(self, result, item, labels):
        info = dict()
        info['path'] = result['path']

        info['source'] = result['url']
        info['md5'] = result['checksum']

        info['labels'] = labels.copy()
        return info


class ImagesInfoPipeline(FilesInfoPipeline):

    DEFAULT_URLS_FIELD = 'image_urls'
    DEFAULT_RESULTS_FIELD = 'images'


class VideosInfoPipeline(FilesInfoPipeline):

    DEFAULT_URLS_FIELD = 'video_url'
    DEFAULT_RESULTS_FIELD = 'video'
