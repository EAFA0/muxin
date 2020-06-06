import yaml


def load_config(config):
    task_config = yaml.safe_load(config)

    task_fields = ['name', 'dataset', 'spiders']
    spider_fields = ['project', 'name']

    for field in task_fields:
        if field not in task_config:
            raise ValueError(f"Crawler task config is missing the {field} field.")

    for spider_config in task_config['spiders']:
        for field in spider_fields:
            if field not in spider_config:
                raise ValueError(f"Crawler config is missing the {field} field.")

    return task_config

def dump_config(config):
    return yaml.safe_dump(config)