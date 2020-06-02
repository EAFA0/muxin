import json
import requests
from scrapyd_api import ScrapydAPI
from collections import defaultdict

from .models import Task as TaskModel
from .models import Spider as SpiderModel

from .serializers import TaskSerializer


scrapyd = ScrapydAPI('http://localhost:6800')


class Task:

    def create(self, task_name: str, dataset: str, **kwargs) -> TaskModel:
        return TaskModel.objects.create(name=task_name, dataset=dataset, **kwargs)

    def running_spiders(self, task_name: str):
        spiders = SpiderModel.objects.filter(task=task_name)
        runnings = Spider.running_spider_set().intersection(
            {spider.id for spider in spiders})

        return {spider for spider in spiders if spider.id in runnings}

    def cancel(self, task_name: str) -> bool:
        for spider in self.running_spiders(task_name):
            scrapyd.cancel(spider.project, spider.id)
        return True


class Spider:

    @classmethod
    def running_spider_set(cls):
        '''
        获得所有正在运行的爬虫id
        '''
        projects = scrapyd.list_projects()
        running_set = set()
        for project in projects:
            result = scrapyd.list_jobs(project)

            spider_list = result['pending'] + result['running']
            running_set.update({item['id'] for item in spider_list})
        return running_set

    def create(self, task_name: str, *, project: str, spider_name: str, **kwargs) -> SpiderModel:
        task_obj = TaskModel.objects.get(name=task_name)

        job_id = scrapyd.schedule(project,
                                  spider_name,
                                  dataset=task_obj.dataset
                                  ** kwargs)

        spider = SpiderModel.objects.create(id=job_id,
                                                 name=spider_name,
                                                 task=task_name,
                                                 project=project)

        return spider

    def cancel(self, spider_id: str) -> SpiderModel:
        spider = SpiderModel.objects.get(id=spider_id)

        if spider_id in self.running_spider_set():
            scrapyd.cancel(spider.project, spider.id)

        return spider

    def log(self, spider_id: str) -> bytes:
        spider = SpiderItem.objects.get(id=spider_id)
        url += f"{spider.name}/{spider.id.hex}.log"
        log = requests.get(url=url, stream=True)
        return log.raw.read()
