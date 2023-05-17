
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile, Comment


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()


@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, **kwargs):
    if instance.post.author.email != instance.email:
        send_mail(
            'Новый комментарий к вашему посту',
            f'Пользователь {instance.name} оставил комментарий к вашему посту "{instance.post.title}"',
            'от кого <отправитель@домен.com>',
            [instance.post.author.email],
            fail_silently=False,
        )