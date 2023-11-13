from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Post(models.Model):
    TYPE = (
        ('tank', 'Танки'),
        ('heal', 'Хилы'),
        ('dd', 'ДД'),
        ('buyers', 'Торговцы'),
        ('gildemaster', 'Гилдмастеры'),
        ('quest', 'Квестгиверы'),
        ('smith', 'Кузнецы'),
        ('tanner', 'Кожевники'),
        ('potion', 'Зельевары'),
        ('spellmaster', 'Мастера заклинаний'),
    )

    author_post = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True,
                                    null=True, verbose_name='Автор')
    date_time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    category_post = models.CharField(max_length=11, choices=TYPE, default='tank')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')

    def preview(self):
        return f'{self.content[:123]}...'

    def __str__(self):
        return f'{self.title}. Автор: {self.author_post.username}'

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Responses(models.Model):
    res_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    res_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    res_content = models.TextField(verbose_name='Текст отклика')
    date_time_create = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
        ordering = ['-date_time_create']

    def __str__(self):
        return str(self.res_user) + ' responses ' + str(self.res_content)
