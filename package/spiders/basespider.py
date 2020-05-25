from scrapy import Spider

class BaseSpider(Spider):

    file_type = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 强制要求 dataset 字段不为空
        self.dataset = kwargs['dataset']