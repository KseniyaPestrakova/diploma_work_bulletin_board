from django.db import models

from config import settings


class Advertisement(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название товара")
    price = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True, verbose_name="Описание товара")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                               verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-created_at']


class Comment(models.Model):
    text = models.TextField(blank=True, null=True, verbose_name="Описание урока")
    ad = models.ForeignKey(Advertisement, on_delete=models.SET_NULL, blank=True, null=True, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Автор"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Отзыв {self.author} к объявлению {self.ad}'

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"
