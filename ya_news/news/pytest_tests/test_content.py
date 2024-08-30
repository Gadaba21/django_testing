
import pytest
from django.conf import settings
from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_pages_contains_form(author_client, news_detail):
    response = author_client.get(news_detail)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


def test_pages_contains_client_form(client, news_detail):
    response = client.get(news_detail)
    assert 'form' not in response.context


def test_comments_order(client, news, comment_create, news_detail):
    comment_create
    response = client.get(news_detail)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_news_order(client, create_news, news_home):
    create_news
    response = client.get(news_home)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_news_count(client, create_news, news_home):
    create_news
    response = client.get(news_home)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE
