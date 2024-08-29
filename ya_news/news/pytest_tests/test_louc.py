from http import HTTPStatus

import pytest
from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from pytest_django.asserts import assertFormError, assertRedirects


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, form_data, url):
    client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(author_client, news, form_data, author, url):
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == 'Новый текст'
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, url):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(url, data=bad_words_data)
    assertFormError(response, 'form', 'text', errors=(WARNING))
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_edit_comment(
        author_client,
        form_data,
        comment,
        edit_url,
        url
):
    form_data['text'] = 'буб'
    response = author_client.post(edit_url, form_data)
    assertRedirects(response, url + '#comments')
    comment.refresh_from_db()
    assert comment.text == 'буб'


def test_user_cant_edit_comment_of_another_user(
        not_author_client,
        form_data,
        comment,
        edit_url
):
    response = not_author_client.post(edit_url, form_data)
    assert response.status_code, HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == 'Текст комментария'
