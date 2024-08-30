from http import HTTPStatus

import pytest
from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from pytest_django.asserts import assertFormError, assertRedirects

FORM_DATA = {
    'title': 'Новый заголовок',
    'text': 'Новый текст',
}


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news_detail):
    count_comments = Comment.objects.count()
    client.post(news_detail, data=FORM_DATA)
    comments_count = Comment.objects.count()
    assert comments_count == count_comments


def test_user_can_create_comment(author_client,
                                 news,
                                 author,
                                 news_detail):
    count_comments = Comment.objects.count()
    response = author_client.post(news_detail, data=FORM_DATA)
    assertRedirects(response, f'{news_detail}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == count_comments + 1
    comment = Comment.objects.get()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.parametrize(
    'ban',
    BAD_WORDS
)
def test_user_cant_use_bad_words(author_client, news_detail, ban):
    count_comments = Comment.objects.count()
    bad_words_data = {'text': f'Какой-то текст, {ban}, еще текст'}
    response = author_client.post(news_detail, data=bad_words_data)
    assertFormError(response, 'form', 'text', errors=(WARNING))
    comments_count = Comment.objects.count()
    assert comments_count == count_comments


def test_author_can_edit_comment(
        author_client,
        comment,
        news_edit,
        news_detail,
        news,
        author
):
    FORM_DATA['text'] = 'буб'
    response = author_client.post(news_edit, FORM_DATA)
    assertRedirects(response, news_detail + '#comments')
    comment.refresh_from_db()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_edit_comment_of_another_user(
        not_author_client,
        comment,
        news_edit,
        news,
        author
):
    response = not_author_client.post(news_edit, FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment.text != FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_delete_comment_of_another_user(
        author_client,
        news_delete
):
    count_comments = Comment.objects.count()
    author_client.post(news_delete)
    comments_count = Comment.objects.count()
    assert comments_count == count_comments - 1


def test_user_cant_delete_comment_of_not_another_user(
        not_author_client,
        news_delete
):
    count_comments = Comment.objects.count()
    not_author_client.post(news_delete)
    comments_count = Comment.objects.count()
    assert comments_count == count_comments
