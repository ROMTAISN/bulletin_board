# bulletin_board
Проект доски объявлений MMO RPG.
Создано две основные модели в связи с поставленными задачами.
Модель объявления - Post. И модель отклика - Responses.
Модель категорий не создавалась. Категории строго заданы в моделе Post. 
Модель Автор тоже не создавалась. Используется стандартныя модель User.
Поле контента модели Post сделано текстовым, а возможность добавления в него картинок и видео реализовано с помощью django-tinymce.
Отправка пользователям новостных рассылок и отправка уведомления при создании и принятии отклика реализовано через celery b redis.