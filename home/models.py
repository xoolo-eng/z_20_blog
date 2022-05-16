from django.db import models


class FeedBack(models.Model):
    full_name = models.CharField(max_length=256, verbose_name="ФИО")
    email = models.EmailField(verbose_name="Емаил")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Телефон")
    message = models.TextField(verbose_name="Сообщение")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    active = models.BooleanField(default=True, verbose_name="В работе")

    class Meta:
        db_table = "feedback"
        unique_together = ("full_name", "email", "active")
        verbose_name = "Обращение гражданина"
        verbose_name_plural = "Обращения граждан"
