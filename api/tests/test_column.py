import factory.fuzzy
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from .factories import UserFactory, ColumnFactory, BoardFactory
from time import perf_counter


class TestColumnCRUD(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.column = ColumnFactory()
        self.board = BoardFactory()

        self.client.force_authenticate(user=self.user)
        self.url = reverse('column-api', kwargs={'pk': self.column.pk})
        self.list_creation_url = reverse('column-list-api')

    def test_get_list_board(self):
        start = perf_counter()
        response = self.client.get(self.list_creation_url)
        end = perf_counter()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.data.get('data')), list)
        self.assertLess(end - start, 0.2)

    def test_get_column(self):
        expected = 3

        start = perf_counter()
        response = self.client.get(self.url)
        end = perf_counter()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), expected)
        self.assertLess(end-start, 0.2)

    def test_create_column(self):
        expected = 2
        new_column = model_to_dict(ColumnFactory())
        new_column.pop('id')

        start = perf_counter()
        response = self.client.post(self.list_creation_url, data=new_column)
        end = perf_counter()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, new_column)
        self.assertEqual(len(response.data), expected)
        self.assertLess(end-start, 0.2)

    def test_fill_update(self):
        expected = 2
        new_column = model_to_dict(ColumnFactory())
        new_column.pop('id')

        start = perf_counter()
        response = self.client.put(self.url, data=new_column)
        end = perf_counter()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, new_column)
        self.assertEqual(len(response.data), expected)
        self.assertLess(end-start, 0.2)

    def test_partial_update(self):
        expected = 1
        new_title = {'title': 'new_test_title'}

        start = perf_counter()
        response = self.client.patch(self.url, data=new_title)
        end = perf_counter()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), new_title.get('title'))
        self.assertEqual(len(response.data), expected)
        self.assertLess(end - start, 0.2)

    def test_delete(self):
        start = perf_counter()
        response = self.client.delete(self.url)
        end = perf_counter()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertLess(end - start, 0.2)
