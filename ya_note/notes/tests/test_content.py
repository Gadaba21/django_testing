
from notes.forms import NoteForm

from .common import BaseTestCase


class TestRoutes(BaseTestCase):

    def test_authorized_client_has_form(self):
        urls = (
            (self.note_add, self.note_edit)
        )
        for name in urls:
            with self.subTest(name=name):
                response = self.auth_client.get(name)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)

    def test_notes_list_for_different_users(self):
        response = self.auth_client.get(self.note_list)
        object_list = response.context['object_list']
        self.assertTrue(self.note in object_list)
        response = self.reader_client.get(self.note_list)
        self.assertFalse(self.note in response.context['object_list'])
