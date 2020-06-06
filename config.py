import yaml


class Config:
    DJANGO_PORT = None
    SCRAPYD_PORT = None

    MYSQL_HOST = None
    MYSQL_PORT = None
    MYSQL_USER = None
    MYSQL_PASSWORD = None
    MYSQL_DATABASE = None

    SCRAPYD_SERVER = None
    DATASET_SERVER = None

    instance = None

    def __new__(cls, *arg, **kwargs):
        if cls.instance:
            return cls.instance
        
        with open('./config.yaml') as config_file:
            config = yaml.safe_load(config_file)

        cls.DJANGO_PORT = config['django']['server_port']
        cls.SCRAPYD_PORT = config['scrapyd']['http_port']
        cls.DATASET_SERVER = "http://localhost:{}".format(cls.DJANGO_PORT)
        cls.SCRAPYD_SERVER = "http://localhost:{}/dataset".format(cls.SCRAPYD_PORT)

        mysql_config = config['mysql']
        cls.MYSQL_HOST = mysql_config['host']
        cls.MYSQL_PORT = mysql_config['port']
        cls.MYSQL_USER = mysql_config['user']
        cls.MYSQL_PASSWORD = mysql_config['password']
        cls.MYSQL_DATABASE = mysql_config['database']

        cls.instance = object.__new__(cls, *arg, **kwargs)
        return cls.instance

def get_config():
    return Config()