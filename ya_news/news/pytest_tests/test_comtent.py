from datetime import timedelta

import pytest
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from news.forms import CommentForm
from news.models import News


@pytest.mark.django_db
def test_pages_contains_form(author_client, news):
    url = reverse('news:detail', args=(news.id,))
    response = author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


@pytest.mark.django_db
def test_pages_contains_client_form(client, news):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert 'form' not in response.context
    assert not isinstance(response.context.get('form'), CommentForm)


@pytest.mark.django_db
def test_comments_order(client, news, comment):
    for index in range(10):
        comment = comment
        comment.created = timezone.now() + timedelta(days=index)
        comment.save()
    response = client.get(reverse('news:detail', args=(news.id,)))
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
def test_news_order(client, create_news):
    News.objects.bulk_create(create_news)
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_news_count(client, create_news):
    News.objects.bulk_create(create_news)
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE
