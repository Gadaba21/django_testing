from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from notes.models import Note

SLUG_CONSTANCE = 'gf'
NOTES_ADD = reverse('notes:add')
NOTES_EDIT = reverse('notes:edit', kwargs={'slug': SLUG_CONSTANCE})
NOTES_DELETE = reverse('notes:delete', kwargs={'slug': SLUG_CONSTANCE})
NOTES_DETAIL = reverse('notes:detail', kwargs={'slug': SLUG_CONSTANCE})
NOTES_LIST = reverse('notes:list')
NOTES_SUCCESS = reverse('notes:success')
NOTES_HOME = reverse('notes:home')


class BaseTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug=SLUG_CONSTANCE,
            author=cls.author
        )
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note_add = NOTES_ADD
        cls.note_edit = NOTES_EDIT
        cls.note_delete = NOTES_DELETE
        cls.note_detail = NOTES_DETAIL
        cls.note_list = NOTES_LIST
        cls.note_success = NOTES_SUCCESS
        cls.note_home = NOTES_HOME
