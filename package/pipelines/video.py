import os
import shutil
from hashlib import md5
from pathlib import Path

import youtube_dl
from you_get import common

from scrapy import Spider
from scrapy.http import Request, Response
from scrapy.settings import Settings
from scrapy.utils.misc import md5sum
from scrapy.responsetypes import responsetypes
from scrapy.pipelines.files import FilesPipeline, FSFilesStore

from package.utils.dict import merge
from package.utils.url import id_from_url


class VideoNotDownload(Exception):
    pass


class VideoDownloader:

    default_opts = {}
    download_opts_field = 'download_opts'

    cache_dir = None

    def __init__(self, settings: Settings):
        cache_dir = settings.get('VIDEOS_CACHE_DIR', './')
        self.cache_dir = Path(cache_dir)

        if not self.cache_dir.exists():
            self.cache_dir.mkdir(parents=True)

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def download_func(self, download_url: str, download_opts: dict) -> str:
        '''
        实际的下载函数, 返回一个 Response
        '''
        raise NotImplementedError

    def download_request(self, request, spider):
        if self.download_opts_field in request.meta:
            opts = request.meta[self.download_opts_field]
            download_opts = merge(self.default_opts, opts)
        else:
            download_opts = self.default_opts

        download_url = request.url
        download_path = self.download_func(download_url, download_opts)

        respcls = responsetypes.from_mimetype('text/*')
        response = respcls(request=request,
                           url=download_url,
                           encoding='utf-8',
                           body=download_path)

        return response

    @classmethod
    def complete_absolute_path(cls, path: Path, filename: str, ext: str = ''):
        '''
        base on pathlib.Path.glob

        return the absolute path of first file matched.
        '''
        filepaths = list(path.glob(f"{filename}*{ext}"))
        if filepaths != []:
            return str(filepaths[0].absolute())
        else:
            raise VideoNotDownload


class YoutubeDL(VideoDownloader):

    default_opts = {
        'outtmpl': '%(id)s.%(ext)s'
    }

    def youtube_dl_opts(self, download_opts: dict):
        filename = download_opts['outtmpl']

        download_opts['outtmpl'] = str(self.cache_dir / filename)
        return download_opts

    def download_func(self, download_url: str, download_opts: dict) -> str:
        opts = self.youtube_dl_opts(download_opts)
        with youtube_dl.YoutubeDL(opts) as ydl:
            info_dict = ydl.extract_info(download_url)

        filename = info_dict['id']
        return self.complete_absolute_path(self.cache_dir, filename)


class YouGet(VideoDownloader):

    default_opts = {
        'merge': True,
        'caption': False
    }

    def download_func(self, download_url: str, download_opts: dict) -> str:
        download_opts['output_dir'] = str(self.cache_dir)

        # 如果该视频不在缓存目录中
        filename = id_from_url(download_url)
        if list(self.cache_dir.glob(f"{filename}.*")) == []:
            # you_get 特有的设置输出文件方式 =.=
            common.output_filename = filename
            common.download_main(
                common.any_download, None,
                [download_url], None, **download_opts)

        return self.complete_absolute_path(self.cache_dir, filename)


class VideosPipeline(FilesPipeline):

    downloaders = {
        'youtube-dl': YoutubeDL,
        'you-get': YouGet
    }

    def __init__(self, store_uri, download_func=None, settings=None):
        self.videos_urls_field = settings.get(
            'VIDEOS_URLS_FIELD', 'videos_urls'
        )
        self.videos_result_field = settings.get(
            'VIDEOS_RESULT_FIELD', 'videos'
        )

        super().__init__(store_uri,
                         settings=settings,
                         download_func=self.video_downloader)

    @classmethod
    def from_settings(cls, settings):
        # Similar with ImagesPipeline.
        s3store = cls.STORE_SCHEMES['s3']
        s3store.AWS_ACCESS_KEY_ID = settings['AWS_ACCESS_KEY_ID']
        s3store.AWS_SECRET_ACCESS_KEY = settings['AWS_SECRET_ACCESS_KEY']
        s3store.AWS_ENDPOINT_URL = settings['AWS_ENDPOINT_URL']
        s3store.AWS_REGION_NAME = settings['AWS_REGION_NAME']
        s3store.AWS_USE_SSL = settings['AWS_USE_SSL']
        s3store.AWS_VERIFY = settings['AWS_VERIFY']
        s3store.POLICY = settings['VIDEOS_STORE_S3_ACL']

        gcs_store = cls.STORE_SCHEMES['gs']
        gcs_store.GCS_PROJECT_ID = settings['GCS_PROJECT_ID']
        gcs_store.POLICY = settings['VIDEOS_STORE_GCS_ACL'] or None

        ftp_store = cls.STORE_SCHEMES['ftp']
        ftp_store.FTP_USERNAME = settings['FTP_USER']
        ftp_store.FTP_PASSWORD = settings['FTP_PASSWORD']
        ftp_store.USE_ACTIVE_MODE = settings.getbool('FEED_STORAGE_FTP_ACTIVE')

        store_uri = settings['VIDEOS_STORE']

        for downloader in cls.downloaders:
            obj = cls.downloaders[downloader]
            cls.downloaders[downloader] = obj.from_settings(settings)

        return cls(store_uri, cls.video_downloader, settings=settings)

    def video_downloader(self, request: Request, spider: Spider) -> Response:
        # Request.meta['download_tool']: youtube_dl or you_get or whatever.
        # Request.meta['download_opts']: download options of the download_tool.

        # Response.body <- local path of video

        downloader_name = request.meta['download_tool']
        try:
            downloder = self.downloaders[downloader_name]
        except KeyError:
            raise KeyError('No such download tool')

        return downloder.download_request(request, spider)

    def file_downloaded(self, response, request, info):
        return self.video_downloaded(response, request, info)

    def video_downloaded(self, response, request, info):
        def remove_file(buf, path):
            buf.close()
            os.remove(path)

        dst_path = self.file_path(request, response=response, info=info)
        local_path = response.text

        if isinstance(self.store, FSFilesStore):
            dst = self.store._get_filesystem_path(dst_path)
            shutil.move(local_path, dst)
        else:
            # 此处有一个无法删除最后一个文件的 bug
            buf = open(local_path, 'rb')
            self.store.persist_file(dst_path, buf, info).addCallback(
                remove_file, buf, local_path)

        return self.video_cheksum(response, info.spider)

    def file_path(self, request, response=None, info=None):
        if response is None:
            return None

        filename = response.meta['info']['id']
        ext = response.text.split('.')[-1]
        return f'{filename}.{ext}'

    def video_cheksum(self, response, spider) -> str:
        video_info = response.meta['info']
        source = spider.name
        _id = video_info['id']

        video_id = bytes(source + _id, encoding='utf-8')
        return md5(video_id).hexdigest()

    def get_media_requests(self, item, info):
        meta = item['meta'] if 'meta' in item else {}

        item_urls = item[self.videos_urls_field]
        for item_url in item_urls:
            yield Request(item_url, meta=meta)

    def item_completed(self, results, item, info):
        if isinstance(item, dict) or self.videos_result_field in item.fields:
            item[self.videos_result_field] = [x for ok, x in results if ok]
        return item
