from http import HTTPStatus

from django.urls import reverse

from .common import BaseTestCase


class TestRoutes(BaseTestCase):

    def test_home_page(self):
        urls = (
            ('notes:home'),
            ('users:login'),
            ('users:logout'),
            ('users:signup'),
        )
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_node_edit_and_delete(self):
        urls = (
            (self.note_add, self.author, HTTPStatus.OK),
            (self.note_edit, self.author, HTTPStatus.OK),
            (self.note_delete, self.author, HTTPStatus.OK),
            (self.note_detail, self.author, HTTPStatus.OK),
            (self.note_list, self.author, HTTPStatus.OK),
            (self.note_success, self.author, HTTPStatus.OK),
            (self.note_home, self.author, HTTPStatus.OK),
            (self.note_add, self.reader, HTTPStatus.OK),
            (self.note_edit, self.reader, HTTPStatus.NOT_FOUND),
            (self.note_delete, self.reader, HTTPStatus.NOT_FOUND),
            (self.note_detail, self.reader, HTTPStatus.NOT_FOUND),
            (self.note_list, self.reader, HTTPStatus.OK),
            (self.note_success, self.reader, HTTPStatus.OK),
            (self.note_home, self.reader, HTTPStatus.OK),
        )
        for name, reader, status in urls:
            self.client.force_login(reader)
            with self.subTest(reader=reader, name=name, status=status):
                response = self.client.get(name)
                self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')
        urls = (
            (self.note_detail),
            (self.note_delete),
            (self.note_detail),
            (self.note_list),
            (self.note_success)
        )
        for name in urls:
            with self.subTest(name=name):
                redirect_url = f'{login_url}?next={name}'
                response = self.client.get(name)
                self.assertRedirects(response, redirect_url)
