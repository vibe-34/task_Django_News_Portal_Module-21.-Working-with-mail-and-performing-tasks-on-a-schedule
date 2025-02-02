from django.db.models.signals import post_save
from django.dispatch import receiver

from.models import Post


@receiver(post_save, sender=Post)
def post_created(instance, **kwargs):
    print('Создана публикация', instance)
