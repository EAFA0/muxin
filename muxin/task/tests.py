from django.test import TestCase
from requests import Session

# Create your tests here.


class TestTask(TestCase):

    def setUp(self):
        self.session = Session()
        return super().setUp()

    def test_task_get(self):
        forms = {
            "name": "hello0"
        }
        files = {
            "args": open('./spider/tests.py'),
            # "file0" : open('./spider/models.py'),
            # "file1": open('./spider/apps.py'),
        }
        response = self.session.post(
            'http://localhost:8000/spider/hello0.json', data=forms, files=files)
        print(response.text[:600])
