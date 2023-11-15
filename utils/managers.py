import datetime

from django.utils.datetime_safe import strftime

from meetmax.settings import MEDIA_ROOT


class MediaPath:
	def __init__(self, directory_name):
		super().__init__()
		self.directory_name = directory_name
		self.now = datetime.datetime.now()

	def directory_path_datatime(self, instance, filename):
		path_url = f'{instance._meta.model_name}/{self.directory_name}/%Y/%m/%d/user_{instance.user.username}/{filename}'
		return strftime(self.now, path_url)





