import json
import requests

from io import BytesIO
from twisted.internet import threads

from config import DATASET_SERVER


class DataSetPipeline:

    def __init__(self, settings):
        self.project_name = settings['BOT_NAME']
        self.target = DATASET_SERVER

        if self.target is None:
            raise ValueError("the settings of DATASET_ENDPOINT is None.")

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def process_item(self, infos, spider):
        for info in infos:
            info['crawler'] = f"{self.project_name}/{spider.name}"

        return self.upload_to_dataset(spider.dataset, infos)

    def upload_to_dataset(self, dataset, infos: list):
        target_url = f"{self.target}/{dataset}/file/"
        defer = threads.deferToThread(
            requests.put, target_url, json=infos)

        defer.addCallback(self.upload_success)
        defer.addErrback(self.upload_failed)
        return defer

    def upload_success(self, response):
        print(response.text)

    def upload_failed(self, failure):
        print(failure)
