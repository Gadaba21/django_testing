
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

    def test_notes_list_for_auth_client(self):
        self.assertTrue(self.note in self.auth_client.get(
            self.note_list).context['object_list'])

    def test_notes_list_for_reader_client(self):
        self.assertFalse(self.note in self.reader_client.get(
            self.note_list).context['object_list'])
