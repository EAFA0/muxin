import json
import requests

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.job import Job

from config import get_config


class SchedulerAPIView(APIView):

    _task_api = get_config().SPIDER_TASK_SERVER

    _job_args = dict(
        date=['run_date', 'timezone'],
        cron=['year', 'month', 'day', 'week', 'day_of_week',
              'hour', 'minute', 'second', 'start_date', 'end_date',
              'timezone', 'jitter'],
        interval=['weeks', 'days', 'hours', 'minutes', 'seconds',
                  'start_date', 'end_date', 'timezone', 'jitter']
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Config = get_config()
        mysql_url = (f'mysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}'
                     f'@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}'
                     f'/{Config.MYSQL_DATABASE}')

        jobstore = SQLAlchemyJobStore(url=mysql_url)

        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(jobstore)
        scheduler.start()

        self.scheduler = scheduler

    def _request_body_to_job_args(self, request_body: dict) -> dict:
        def copy_vaule(_keys: list):
            # 这里还需要一些参数校验, 或者类型转换, 使用一个类专门处理反序列化操作更好
            kwargs = {key: request_body[key]
                      for key in _keys if key in request_body}
            kwargs['trigger'] = job_type
            return kwargs

        if 'method' in request_body:
            job_type = request_body['method']
        else:
            return dict(trigger='date')
        return copy_vaule(self._job_args[job_type])

    def _serialize_job(self, job: Job):
        return dict(id=job.id, next_run_time=job.next_run_time.timestamp())


class SchedulerRetrieveDeleteAPIView(SchedulerAPIView):

    def get(self, request, id, format=None):
        job = self.scheduler.get_job(id)

        return Response(self._serialize_job(job),
                        status=status.HTTP_200_OK)

    def delete(self, request, id, format=None):
        self.scheduler.remove_job(id)
        return Response(status=status.HTTP_200_OK)


class SchedulerCreateListAPIView(SchedulerAPIView):

    def get(self, request, format=None):
        jobs_json = [self._serialize_job(job)
                     for job in self.scheduler.get_jobs()]
        return Response(jobs_json, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        request_body = request.data
        # 提取其中的 task 字段
        task = request.GET['task']
        task_schedule_api = self._task_api.format(task)

        job_kwargs = self._request_body_to_job_args(request_body)
        job = self.scheduler.add_job(requests.post, args=[task_schedule_api],
                                     **job_kwargs)

        return Response(dict(id=job.id), status=status.HTTP_201_CREATED)
