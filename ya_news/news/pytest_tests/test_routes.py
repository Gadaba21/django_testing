from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

HOME = pytest.lazy_fixture('news_home')
LOGIN = pytest.lazy_fixture('user_login')
LOGOUT = pytest.lazy_fixture('user_logout')
SIGNUP = pytest.lazy_fixture('user_signup')
DELETE = pytest.lazy_fixture('news_delete')
EDIT = pytest.lazy_fixture('news_edit')
NOT_AUTHOR_NEWS = pytest.lazy_fixture('not_author_client')
AUTHOR_NEWS = pytest.lazy_fixture('author_client')


@pytest.mark.parametrize(
    'name, parametrized_client, expected_status',
    ((HOME, NOT_AUTHOR_NEWS, HTTPStatus.OK),
     (LOGIN, NOT_AUTHOR_NEWS, HTTPStatus.OK),
     (LOGOUT, NOT_AUTHOR_NEWS, HTTPStatus.OK),
     (SIGNUP, NOT_AUTHOR_NEWS, HTTPStatus.OK),
     (DELETE, NOT_AUTHOR_NEWS, HTTPStatus.NOT_FOUND),
     (EDIT, NOT_AUTHOR_NEWS, HTTPStatus.NOT_FOUND),
     (HOME, AUTHOR_NEWS, HTTPStatus.OK),
     (LOGIN, AUTHOR_NEWS, HTTPStatus.OK),
     (LOGOUT, AUTHOR_NEWS, HTTPStatus.OK),
     (SIGNUP, AUTHOR_NEWS, HTTPStatus.OK),
     (DELETE, AUTHOR_NEWS, HTTPStatus.OK),
     (EDIT, AUTHOR_NEWS, HTTPStatus.OK),
     ))
def test_pages_availability_for_auth_user(
    parametrized_client,
    name,
    expected_status
):
    response = parametrized_client.get(name)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    (DELETE, EDIT)
)
def test_redirects(client, name, user_login):
    expected_url = f'{user_login}?next={name}'
    response = client.get(name)
    assertRedirects(response, expected_url)
