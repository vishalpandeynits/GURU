from django.conf import settings
from django.core.files.storage import FileSystemStorage
from storages.backends.s3boto3 import S3Boto3Storage

if settings.PRODUCTION:
    class PrivateMediaStorage(S3Boto3Storage):
        location = settings.AWS_PRIVATE_MEDIA_LOCATION
        default_acl = 'private'
        file_overwrite = False
        custom_domain = False

    class PublicMediaStorage(S3Boto3Storage):
        location = settings.AWS_PUBLIC_MEDIA_LOCATION
        file_overwrite = False
else:
    PrivateMediaStorage = FileSystemStorage