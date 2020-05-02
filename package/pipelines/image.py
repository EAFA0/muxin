from scrapy.pipelines.images import ImagesPipeline as BaseImagesPipeline


class ImagesPipeline(BaseImagesPipeline):

    def media_downloaded(self, response, request, info):
        # 在此提取已下载图片的信息
        result = super().media_downloaded(response, request, info)
        return result
