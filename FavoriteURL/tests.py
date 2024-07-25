from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from FavoriteURL.models import Favorite_Url, Category, Tags
import json

class FavoriteURLTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='kitipob', password='watanaluk')
        self.client.login(username='kitipob', password='watanaluk')
        self.favorite_url = Favorite_Url.objects.create(url_favorite='https://google.com')

    def test_get_favorite_urls(self):
        response = self.client.get(reverse('favorite_url'))
        self.assertEqual(response.status_code, 200)

    def test_create_favorite_url(self):
        data = {'url_favorite': 'http://github.com'}
        response = self.client.post(reverse('favorite_url'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Favorite_Url.objects.filter(url_favorite='http://github.com').exists())

    def test_update_favorite_url(self):
        data = {'url_favorite': 'https://www.unrealengine.com/en-US'}
        response = self.client.patch(reverse('favorite_url') + f'?id={self.favorite_url.id}', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.favorite_url.refresh_from_db()
        self.assertEqual(self.favorite_url.url_favorite, 'https://www.unrealengine.com/en-US')

    def test_delete_favorite_url(self):
        response = self.client.delete(reverse('favorite_url') + f'?id={self.favorite_url.id}')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Favorite_Url.objects.filter(id=self.favorite_url.id).exists())

class CategoryTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='kitipob', password='watanaluk')
        self.client.login(username='kitipob', password='watanaluk')
        self.category = Category.objects.create(type_name='Computer')

    def test_get_categories(self):
        response = self.client.get(reverse('category'))
        self.assertEqual(response.status_code, 200)

    def test_create_category(self):
        data = {'category': 'Book'}
        response = self.client.post(reverse('category'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Category.objects.filter(type_name='Book').exists())

    def test_update_category(self):
        data = {'category': 'NoteBook'}
        response = self.client.patch(reverse('category') + f'?id={self.category.id}', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.category.refresh_from_db()
        self.assertEqual(self.category.type_name, 'NoteBook')

    def test_delete_category(self):
        response = self.client.delete(reverse('category') + f'?id={self.category.id}')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())

class TagsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='kitipob', password='watanaluk')
        self.client.login(username='kitipob', password='watanaluk')
        self.tag = Tags.objects.create(tage_name='IT')

    def test_get_tags(self):
        response = self.client.get(reverse('tags'))
        self.assertEqual(response.status_code, 200)

    def test_create_tag(self):
        data = {'tag': 'TI 2024'}
        response = self.client.post(reverse('tags'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Tags.objects.filter(tage_name='TI 2024').exists())

    def test_update_tag(self):
        data = {'tag': 'IT Super'}
        response = self.client.patch(reverse('tags') + f'?id={self.tag.id}', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.tage_name, 'IT Super')

    def test_delete_tag(self):
        response = self.client.delete(reverse('tags') + f'?id={self.tag.id}')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Tags.objects.filter(id=self.tag.id).exists())

class CheckUrlsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='kitipob', password='watanaluk')
        self.client.login(username='kitipob', password='watanaluk')

    def test_check_urls(self):
        response = self.client.get(reverse('check_urls'))
        self.assertEqual(response.status_code, 200)
