import yaml


class Config:

    _instance = None
    _django_host = "http://localhost"

    def __new__(cls, *arg, **kwargs):
        if cls._instance:
            return cls._instance
        
        with open('./config.yaml') as config_file:
            config = yaml.safe_load(config_file)

        cls.DJANGO_PORT = config['django']['server_port']
        cls.SCRAPYD_PORT = config['scrapyd']['http_port']
        cls.SCRAPYD_SERVER = f"{cls._django_host}:{cls.SCRAPYD_PORT}"

        cls.DJANGO_SERVER = f"{cls._django_host}:{cls.DJANGO_PORT}"
        cls.DATASET_SERVER = f"{cls.DJANGO_SERVER}/dataset"
        cls.SPIDER_TASK_SERVER = f"{cls.DJANGO_SERVER}/task/{{}}/schedule"

        mysql_config = config['mysql']
        cls.MYSQL_HOST = mysql_config['host']
        cls.MYSQL_PORT = mysql_config['port']
        cls.MYSQL_USER = mysql_config['user']
        cls.MYSQL_PASSWORD = mysql_config['password']
        cls.MYSQL_DATABASE = mysql_config['database']

        cls._instance = object.__new__(cls, *arg, **kwargs)
        return cls._instance

def get_config():
    return Config()