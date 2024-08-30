from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )


@pytest.fixture
def form_comment():
    return {
        'text': 'Новый текст',
    }


@pytest.fixture
def create_news():
    News.objects.bulk_create(News(
        title=f'Новость {index}',
        text='Просто текст.',
        date=datetime.today() - timedelta(days=index)
    )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def news_detail(news):
    url = reverse('news:detail', args=(news.id,))
    return url


@pytest.fixture
def news_delete(comment):
    url = reverse('news:delete', args=(comment.id,))
    return url


@pytest.fixture
def news_edit(comment):
    url = reverse('news:edit', args=(comment.id,))
    return url


@pytest.fixture
def news_home():
    return reverse('news:home')


@pytest.fixture
def user_login():
    return reverse('users:login')


@pytest.fixture
def user_logout():
    return reverse('users:logout')


@pytest.fixture
def user_signup():
    return reverse('users:signup')


@pytest.fixture
def comment_create(news, author):
    for index in range(10):
        Comment.objects.create(news=news, text=index, author=author)
