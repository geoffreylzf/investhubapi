from django.conf import settings


def build_image_path(request, path):
    return request.build_absolute_uri(settings.MEDIA_URL + path)
