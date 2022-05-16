from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch.dispatcher import receiver


class User(AbstractUser):
    phone = models.CharField(max_length=20, verbose_name="User Phone")

    class Meta:
        db_table = "users"
        verbose_name = "User"

    def __str__(self):
        return self.username


@receiver(models.signals.pre_save, sender=User)
def to_hash_password(sender, instance, **kwargs):
    if (instance.id is None) or (sender.objects.get(id=instance.id).password != instance.password):
        instance.set_password(instance.password)


@receiver(models.signals.pre_save, sender=User)
def send_email(sender, instance, **kwargs):
    ...
