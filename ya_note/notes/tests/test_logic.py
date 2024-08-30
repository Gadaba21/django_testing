from http import HTTPStatus

from notes.forms import WARNING
from notes.models import Note
from pytils.translit import slugify

from .common import SLUG_CONSTANCE, BaseTestCase


class TestNotesCreation(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.form_data = {
            'title': 'Заголовок',
            'text': 'Текст',
            'slug': SLUG_CONSTANCE,
        }

    def test_anonymous_user_cant_create_notes(self):
        count_note = Note.objects.count()
        self.client.post(self.note_add, data=self.form_data)
        note_count = Note.objects.count()
        self.assertEqual(note_count, count_note)

    def test_user_can_create_notes(self):
        Note.objects.all().delete()
        self.form_data['title'] = 'fdf'
        response = self.auth_client.post(self.note_add, data=self.form_data)
        self.assertRedirects(response, '/done/')
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.author, self.author)
        self.assertEqual(note.slug, SLUG_CONSTANCE)

    def test_not_unique_slug(self):
        response = self.auth_client.post(self.note_add, data=self.form_data)
        self.assertFormError(response, 'form', 'slug',
                             errors=[f'{SLUG_CONSTANCE}{WARNING}'])
        self.assertEqual(Note.objects.count(), 1)

    def test_empty_slug(self):
        Note.objects.all().delete()
        self.form_data.pop('slug')
        response = self.auth_client.post(self.note_add,
                                         data=self.form_data)
        self.assertRedirects(response, '/done/')
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)
        new_note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)


class TestNoteEditDelete(BaseTestCase):

    NOTE_TEXT = 'Текст'
    NEW_NOTE_TEXT = 'Текст2'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.form_data = {
            'title': 'Заголовок',
            'text': cls.NEW_NOTE_TEXT,
            'slug': SLUG_CONSTANCE,
        }

    def test_author_can_delete_note(self):
        count_note = Note.objects.count()
        response = self.auth_client.delete(self.note_delete)
        self.assertRedirects(response, '/done/')
        note_count = Note.objects.count()
        self.assertEqual(note_count, count_note - 1)

    def test_user_cant_delete_note_of_another_user(self):
        count_note = Note.objects.count()
        response = self.reader_client.delete(self.note_delete)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_count = Note.objects.count()
        self.assertEqual(note_count, count_note)

    def test_author_can_edit_note(self):
        response = self.auth_client.post(self.note_edit, data=self.form_data)
        self.assertRedirects(response, '/done/')
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NEW_NOTE_TEXT)

    def test_user_cant_edit_note_of_another_user(self):
        response = self.reader_client.post(self.note_edit, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NOTE_TEXT)
