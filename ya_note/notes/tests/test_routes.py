from http import HTTPStatus

from .common import BaseTestCase


class TestRoutes(BaseTestCase):

    def test_availability_for_node_edit_and_delete(self):
        urls_client_status = (
            (self.note_add, self.auth_client, HTTPStatus.OK),
            (self.note_edit, self.auth_client, HTTPStatus.OK),
            (self.note_delete, self.auth_client, HTTPStatus.OK),
            (self.note_detail, self.auth_client, HTTPStatus.OK),
            (self.note_list, self.auth_client, HTTPStatus.OK),
            (self.note_success, self.auth_client, HTTPStatus.OK),
            (self.note_home, self.auth_client, HTTPStatus.OK),
            (self.note_add, self.reader_client, HTTPStatus.OK),
            (self.note_edit, self.reader_client, HTTPStatus.NOT_FOUND),
            (self.note_delete, self.reader_client, HTTPStatus.NOT_FOUND),
            (self.note_detail, self.reader_client, HTTPStatus.NOT_FOUND),
            (self.note_list, self.reader_client, HTTPStatus.OK),
            (self.note_success, self.reader_client, HTTPStatus.OK),
            (self.note_home, self.reader_client, HTTPStatus.OK),
            (self.note_home, self.client, HTTPStatus.OK),
            (self.user_login, self.client, HTTPStatus.OK),
            (self.user_logout, self.client, HTTPStatus.OK),
            (self.user_signup, self.client, HTTPStatus.OK),
        )
        for url, client, status in urls_client_status:
            with self.subTest(client=client, url=url, status=status):
                response = client.get(url)
                self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        urls = (
            (self.note_detail),
            (self.note_delete),
            (self.note_detail),
            (self.note_list),
            (self.note_success)
        )
        for name in urls:
            with self.subTest(name=name):
                redirect_url = f'{self.user_login}?next={name}'
                response = self.client.get(name)
                self.assertRedirects(response, redirect_url)
