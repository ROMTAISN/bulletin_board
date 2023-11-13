import datetime
from datetime import datetime
from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from BullBoard import settings
from .models import Post, Responses


@shared_task
def send_email_response(pk):
    response = Responses.objects.get(pk=pk)
    res = response.res_content
    user = response.res_post.author_post.email
    post = response.res_post.title
    html_content = render_to_string(
        'response_created_email.html',
        {
            'text': res,
            'post': post,
            'link': f'{settings.SITE_URL}/responses'
        }
    )
    msg = EmailMultiAlternatives(
        subject=response,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user],
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_response_accept(pk):
    response = Responses.objects.get(pk=pk)
    res = response.res_content
    user = response.res_user.email
    post = response.res_post.title
    post_id = response.res_post.id
    html_content = render_to_string(
        'response_accept.html',
        {
            'text': res,
            'post': post,
            'link': f'{settings.SITE_URL}/{post_id}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=response,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user],
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_message_every_week():
    users_email = User.objects.values_list('email', flat=True)
    for user in users_email:
        today = datetime.datetime.now()
        last_week = today - datetime.timedelta(days=7)
        posts = Post.objects.filter(date_time_create__gte=last_week)
        new_post = []
        for post in posts:
            if post.author_post.email != user:
                new_post.append(post)

        html_content = render_to_string(
            'daily_post.html',
            {
                'link': settings.SITE_URL,
                'posts': new_post,
            },
        )
        msg = EmailMultiAlternatives(
            subject='Статьи за последние 7 дней!',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
