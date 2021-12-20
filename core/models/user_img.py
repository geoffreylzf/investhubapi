import uuid

from django.db import models

from investhubapi.utils.model import CRUSDModel


def image_directory_path(instance, filename):
    arr = filename.split(".")
    name = str(uuid.uuid4()) + "." + arr[-1]
    return 'users/{0}/profile/{1}'.format(instance.created_by.id, name)


class UserImg(CRUSDModel):
    path = models.ImageField(upload_to=image_directory_path)

    class Meta:
        db_table = 'user_img'
        ordering = ['id']
