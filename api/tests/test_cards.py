import factory.fuzzy
from django.core.files.base import ContentFile
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from .factories import UserFactory, ColumnFactory, CardFactory
from time import perf_counter


class TestCardCRUD(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.card = CardFactory()

        self.client.force_authenticate(user=self.user)
        self.url = reverse('card-api', kwargs={'pk': self.card.pk})
        self.list_creation_url = reverse('card-list-api')

    def test_get_list_board(self):
        start = perf_counter()
        response = self.client.get(self.list_creation_url)
        end = perf_counter()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.data.get('data')), list)
        self.assertLess(end - start, 0.2)

    def test_get_card(self):
        expected = 9

        start = perf_counter()
        response = self.client.get(self.url)
        end = perf_counter()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), expected)
        self.assertLess(end - start, 0.2)

    def test_create_column(self):
        expected = 4

        new_card = model_to_dict(CardFactory())
        new_card.pop('id')

        start = perf_counter()
        response = self.client.post(self.list_creation_url, data=new_card)
        end = perf_counter()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, new_card)
        self.assertEqual(len(response.data), expected)
        self.assertLess(end - start, 0.2)

    def test_full_update(self):
        expected = 4
        new_card = model_to_dict(CardFactory())
        new_card.pop('id')

        start = perf_counter()
        response = self.client.put(self.url, data=new_card)
        end = perf_counter()

        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, new_card)
        self.assertEqual(len(response.data), expected)
        self.assertLess(end - start, 0.2)


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



