# Generated by Django 4.2.7 on 2023-11-12 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category_post',
            field=models.CharField(choices=[('tank', 'Танки'), ('heal', 'Хилы'), ('dd', 'ДД'), ('buyers', 'Торговцы'), ('gildemaster', 'Гилдмастеры'), ('quest', 'Квестгиверы'), ('smith', 'Кузнецы'), ('tanner', 'Кожевники'), ('potion', 'Зельевары'), ('spellmaster', 'Мастера заклинаний')], default='tank', max_length=11),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
