import uuid

from django.db import models

from investhubapi.utils.model import CRUSDModel


def image_directory_path(instance, filename):
    arr = filename.split(".")
    name = str(uuid.uuid4()) + "." + arr[-1]
    return 'user/profile/{0}'.format(name)


class UserImg(CRUSDModel):
    path = models.ImageField(upload_to=image_directory_path)

    class Meta:
        db_table = 'user_img'
        ordering = ['id']
