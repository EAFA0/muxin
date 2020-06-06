from io import StringIO

from django.shortcuts import get_object_or_404
from django.core.files import File
from scrapyd_api import ScrapydAPI

from .serializers import TaskSerializer, SpiderSerializer
from .models import Task, Spider

from package.utils.task import load_config
from config import get_config

scrapyd = ScrapydAPI(get_config().SCRAPYD_SERVER)


class TaskAPI:

    @classmethod
    def create(cls, config_file) -> Task:
        task_config = load_config(config_file)
        # 创建本地文件
        task_config['config'] = File(
            config_file, name=f"{task_config['name']}.yaml")

        # 清除 spider 数据
        if 'spiders' in task_config:
            task_config.pop('spiders')

        task_ser = TaskSerializer(data=task_config)

        if task_ser.is_valid():
            return task_ser.save()
        else:
            raise ValueError(task_ser.errors)

    @classmethod
    def start(cls, name: str):
        '''
        启动爬虫任务
        '''
        task = get_object_or_404(Task, pk=name)

        config_str = task.config.open(mode='r').read()
        task_config = load_config(config_str)

        for spider_config in task_config['spiders']:
            SpiderAPI.create(task, spider_config)

        return True

    @classmethod
    def running_spiders(cls, name: str) -> set:
        task = get_object_or_404(Task, pk=name)
        spiders = task.spiders

        runnings = SpiderAPI.running_spider_set().intersection(
            {spider.id for spider in spiders})

        return {spider for spider in spiders if spider.id in runnings}

    @classmethod
    def cancel(cls, name: str) -> bool:
        for spider in cls.running_spiders(name):
            scrapyd.cancel(spider.project, spider.id)
        return True


class SpiderAPI:

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

    @classmethod
    def create(cls, task: Task, spider_config: dict) -> Spider:
        if 'name' not in spider_config or \
                'project' not in spider_config:
            raise ValueError("name 字段和 project 字段缺失")

        # 兼容 scrapyd 接口
        spider_config['spider'] = spider_config.pop('name')
        # 将一个爬虫加入启动队列
        spider_config['id'] = scrapyd.schedule(
            dataset=task.dataset, **spider_config)
        spider_config['name'] = spider_config.pop('spider')

        # 建立 spider 和 task 的关联
        spider_config['task'] = task.name
        spider_ser = SpiderSerializer(data=spider_config)
        if spider_ser.is_valid():
            spider_obj = spider_ser.save()
            # 建立 spider 和 task 之间的关联
            return spider_obj
        else:
            raise ValueError(spider_ser.errors)

    @classmethod
    def cancel(cls, spider_id: str) -> Spider:
        spider = get_object_or_404(Spider, pk=spider_id)

        if spider_id in cls.running_spider_set():
            scrapyd.cancel(spider.project, spider.id)

        return spider

    @classmethod
    def log(cls, spider_id: str) -> str:
        spider = get_object_or_404(Spider, pk=spider_id)
        log_url = f"{scrapyd.target}/{spider.project}/{spider.name}/{spider.id}.log"
        return log_url
