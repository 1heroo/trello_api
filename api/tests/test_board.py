import factory.fuzzy
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from .factories import UserFactory, BoardFactory
from time import perf_counter

from ..models import Board


class TesTBoardCRUD(APITestCase):

    def setUp(self):
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.board = BoardFactory()

        self.url = reverse('board-api', kwargs={'pk': self.board.pk})
        self.list_create_url = reverse('board-list-api')
        self.client.force_authenticate(user=self.user_1)
        self.client.force_authenticate(user=self.user_2)

    def test_get_list_board(self):
        start = perf_counter()
        response = self.client.get(self.list_create_url)
        end = perf_counter()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.data.get('data')), list)
        self.assertLess(end - start, 0.2)

    def test_get_board(self):
        expected = 6

        start = perf_counter()
        response = self.client.get(reverse('board-api', kwargs={'pk': self.board.pk}), format='json')
        end = perf_counter()

        self.assertLess(end - start, 0.2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), expected)

    def test_create_board(self):
        expected = 3
        board = {
            'title': 'TestBoard',
            'author': 1,
            'image': ContentFile(
                    factory.django.ImageField()._make_data(
                        {'width': 1024, 'height': 768}
                    ), 'example.jpg'
            )
        }

        start = perf_counter()
        response = self.client.post(reverse('board-list-api'), data=board, format='multipart')
        end = perf_counter()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), expected)
        self.assertLess(end-start, 0.2)

    def test_full_update(self):
        expected = 4
        new_board = {
            'title': 'NewTestBoard',
            'is_archived': True,
            'image': ContentFile(
                    factory.django.ImageField()._make_data(
                        {'width': 1024, 'height': 768}
                    ), 'example.jpg'
            )
        }
        start = perf_counter()
        response = self.client.put(reverse('board-api', kwargs={'pk': self.board.pk}), data=new_board, format='multipart')
        end = perf_counter()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), expected)
        self.assertLess(end-start, 0.2)

    def test_partial_update(self):
        expected = 1
        new_field = {
            'is_archived': False
        }

        start = perf_counter()
        response = self.client.patch(reverse('board-api', kwargs={'pk': self.board.pk}), data=new_field)
        end = perf_counter()
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_archived'], str(new_field.get('is_archived')))
        self.assertLess(end-start, 0.2)

    def test_board_delete(self):

        start = perf_counter()
        response = self.client.delete(reverse('board-api', kwargs={'pk': self.board.pk}))
        end = perf_counter()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertLess(end-start, 0.2)
