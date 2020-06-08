import os
import yaml
import configparser

from config import get_config


def scrapyd_init(scrapyd_server, scrapy_projects: dict):
    scrapy_config = configparser.ConfigParser()

    for project, settings in scrapy_projects.items():
        # 修改 config 的内容, 生成 default 字段和 project 字段
        scrapy_config['settings'] = dict(default = settings)
        scrapy_config['deploy'] = dict(project=project, url=scrapyd_server)

        with open('./scrapy.cfg', 'w') as scrapy_config_file:
            scrapy_config.write(scrapy_config_file)
        # deploy
        os.system('scrapyd-deploy')
        # 清除项目打包缓存
        os.remove('./setup.py')

    # 删除 scrapy 配置文件
    os.remove('./scrapy.cfg')


def start_django(django_config: dict):
    server_port = django_config['server_port']
    os.system(f'python3 ./manage.py runserver {server_port} &')


def start_scrapyd(scrapyd_config: dict):
    with open('./scrapyd.conf', 'w') as scrapyd_config_file:
        scrapyd_config_parser = configparser.ConfigParser()
        scrapyd_config_parser['scrapyd'] = scrapyd_config
        scrapyd_config_parser.write(scrapyd_config_file)

    os.system('scrapyd -l ./logs/scrapyd.log &')
    os.remove('./scrapyd.conf')


if __name__ == "__main__":
    with open('./config.yaml') as config_file:
        muxin_config = yaml.safe_load(config_file)
    
    start_django(muxin_config['django'])
    start_scrapyd(muxin_config['scrapyd'])
    scrapyd_init(get_config().SCRAPYD_SERVER, muxin_config['scrapy']['projects'])
